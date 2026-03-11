# apps/citas/views.py
import json
from datetime import datetime, timedelta, date, time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from apps.core.decorators import rol_requerido, get_rol
from .models import Cita, Doctor, HorarioDoctor
from .forms import CitaForm


# ── Validar solapamiento de citas (backend) ───────────────────
def _validar_solapamiento(cita_nueva, excluir_pk=None):
    """
    Devuelve mensaje de error si hay solapamiento, None si está libre.
    Maneja correctamente datetimes con y sin timezone (USE_TZ=True).
    """
    from datetime import timedelta
    from django.utils import timezone as tz
    if not cita_nueva.fecha_hora or not cita_nueva.doctor_id:
        return None

    nueva_ini = cita_nueva.fecha_hora
    # Normalizar a aware si es necesario
    if tz.is_naive(nueva_ini):
        nueva_ini = tz.make_aware(nueva_ini)
    nueva_fin = nueva_ini + timedelta(minutes=cita_nueva.duracion_min or 30)

    # Solo comparar citas del mismo día — usar rango local para evitar problema UTC
    fecha_cita = nueva_ini.date()
    from datetime import datetime
    inicio_dia = timezone.make_aware(datetime(fecha_cita.year, fecha_cita.month, fecha_cita.day, 0, 0, 0))
    fin_dia    = timezone.make_aware(datetime(fecha_cita.year, fecha_cita.month, fecha_cita.day, 23, 59, 59))
    qs = Cita.objects.filter(
        doctor=cita_nueva.doctor,
        fecha_hora__gte=inicio_dia,
        fecha_hora__lte=fin_dia,
    ).exclude(estado__in=['CANCELADA', 'NO_ASISTIO'])

    if excluir_pk:
        qs = qs.exclude(pk=excluir_pk)

    for c in qs:
        c_ini = c.fecha_hora
        if tz.is_naive(c_ini):
            c_ini = tz.make_aware(c_ini)
        c_fin = c_ini + timedelta(minutes=c.duracion_min or 30)
        if nueva_ini < c_fin and nueva_fin > c_ini:
            c_ini_local = tz.localtime(c_ini)
            c_fin_local = tz.localtime(c_fin)
            return (
                f'El Dr. {cita_nueva.doctor.apellidos} ya tiene una cita de '
                f'{c_ini_local.strftime("%H:%M")} a {c_fin_local.strftime("%H:%M")} ese día. '
                f'Elige otro horario disponible.'
            )
    return None


# ── AJAX: doctores por especialidad ───────────────────────────
@login_required
def ajax_doctores(request):
    """Devuelve doctores filtrados por especialidad. Muestra todos (activos e inactivos)."""
    especialidad = request.GET.get('especialidad', '').strip()
    qs = Doctor.objects.all().order_by('apellidos')
    if especialidad:
        qs = qs.filter(especialidad__iexact=especialidad)

    data = []
    for d in qs:
        data.append({
            'id':           d.pk,
            'nombre':       f'Dr. {d.apellidos}, {d.nombres}',
            'especialidad': d.especialidad,
            'tiene_horario': d.horarios.exists(),
            'activo':       d.activo,
        })
    return JsonResponse({'doctores': data})


# ── AJAX: horarios disponibles de un doctor en una fecha ──────
@login_required
def ajax_horarios(request):
    """
    Dado un doctor_id, fecha y duracion_min:
    - Verifica que el doctor tenga horario ese día de la semana
    - Obtiene todas las citas activas de ese día
    - Calcula los slots ocupados
    - Devuelve la lista de horas disponibles + la primera sugerida
    - Incluye indicador de carga del doctor (% ocupado del día)
    """
    doctor_id    = request.GET.get('doctor_id')
    fecha_str    = request.GET.get('fecha')       # YYYY-MM-DD
    duracion_min = int(request.GET.get('duracion', 30))

    if not doctor_id or not fecha_str:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    try:
        doctor = Doctor.objects.get(pk=doctor_id)
        fecha  = date.fromisoformat(fecha_str)
    except (Doctor.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Doctor o fecha inválida'}, status=400)

    # Día de semana (0=Lunes ... 6=Domingo)
    dia_semana = fecha.weekday()

    # Verificar que el doctor trabaje ese día
    try:
        horario = doctor.horarios.get(dia_semana=dia_semana)
    except HorarioDoctor.DoesNotExist:
        dia_nombre = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'][dia_semana]
        return JsonResponse({
            'disponible': False,
            'mensaje': f'El Dr. {doctor.apellidos} no atiende los {dia_nombre}s.',
            'slots': [],
            'sugerido': None,
        })

    # Citas activas del doctor en esa fecha
    # IMPORTANTE: Con USE_TZ=True, fecha_hora__date compara en UTC.
    # Usamos rango de datetimes locales convertidos a UTC para obtener el día correcto en Lima.
    from datetime import datetime, timedelta as td2
    inicio_dia = timezone.make_aware(datetime(fecha.year, fecha.month, fecha.day, 0, 0, 0))
    fin_dia    = timezone.make_aware(datetime(fecha.year, fecha.month, fecha.day, 23, 59, 59))

    citas_dia = Cita.objects.filter(
        doctor=doctor,
        fecha_hora__gte=inicio_dia,
        fecha_hora__lte=fin_dia,
    ).exclude(estado__in=['CANCELADA']).order_by('fecha_hora').values('fecha_hora', 'duracion_min')

    # Construir bloques ocupados: lista de (inicio, fin) en minutos desde medianoche (hora local)
    ocupados = []
    for c in citas_dia:
        inicio_dt = c['fecha_hora']
        if timezone.is_aware(inicio_dt):
            inicio_dt = timezone.localtime(inicio_dt)
        ini_min = inicio_dt.hour * 60 + inicio_dt.minute
        fin_min = ini_min + c['duracion_min']
        ocupados.append((ini_min, fin_min))

    # Generar todos los slots cada 10 minutos dentro del horario del doctor
    h_ini = horario.hora_inicio.hour * 60 + horario.hora_inicio.minute
    h_fin = horario.hora_fin.hour   * 60 + horario.hora_fin.minute

    slots = []
    primer_libre = None

    t = h_ini
    while t + duracion_min <= h_fin:
        t_fin = t + duracion_min
        # Verificar conflicto con citas existentes
        libre = True
        for (oc_ini, oc_fin) in ocupados:
            if t < oc_fin and t_fin > oc_ini:
                libre = False
                break

        hora_str     = f"{t // 60:02d}:{t % 60:02d}"
        hora_fin_str = f"{t_fin // 60:02d}:{t_fin % 60:02d}"
        slots.append({
            'hora':     hora_str,
            'hora_fin': hora_fin_str,
            'libre':    libre,
            'label':    f"{hora_str} – {hora_fin_str}",
        })
        if libre and primer_libre is None:
            primer_libre = hora_str
        t += 10  # siempre slots cada 10 min para detectar todos los huecos

    # Calcular carga del doctor ese día
    minutos_totales   = h_fin - h_ini
    minutos_ocupados  = sum(fin - ini for ini, fin in ocupados)
    pct_carga         = round((minutos_ocupados / minutos_totales) * 100) if minutos_totales > 0 else 0

    # Clasificar disponibilidad
    if pct_carga >= 90:
        disponibilidad_label = 'muy_ocupado'
        disponibilidad_texto = 'Muy ocupado'
    elif pct_carga >= 60:
        disponibilidad_label = 'ocupado'
        disponibilidad_texto = 'Disponibilidad limitada'
    elif pct_carga >= 30:
        disponibilidad_label = 'moderado'
        disponibilidad_texto = 'Moderadamente disponible'
    else:
        disponibilidad_label = 'disponible'
        disponibilidad_texto = 'Alta disponibilidad'

    libres_count = sum(1 for s in slots if s['libre'])

    return JsonResponse({
        'disponible':          True,
        'doctor_nombre':       f'Dr. {doctor.apellidos}, {doctor.nombres}',
        'horario_inicio':      horario.hora_inicio.strftime('%H:%M'),
        'horario_fin':         horario.hora_fin.strftime('%H:%M'),
        'slots':               slots,
        'sugerido':            primer_libre,
        'pct_carga':           pct_carga,
        'disponibilidad_label': disponibilidad_label,
        'disponibilidad_texto': disponibilidad_texto,
        'citas_agendadas':     len(ocupados),
        'slots_libres':        libres_count,
    })


# ── Lista de citas ─────────────────────────────────────────────
@login_required
def lista(request):
    rol = get_rol(request.user)

    if rol == 'DOCTOR':
        qs = Cita.objects.filter(doctor__usuario=request.user).select_related('paciente', 'doctor')
    else:
        qs = Cita.objects.select_related('paciente', 'doctor')

    qs = qs.order_by('-fecha_hora')

    q      = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')
    fecha  = request.GET.get('fecha', '')
    if q:
        qs = qs.filter(
            Q(paciente__nombres__icontains=q) |
            Q(paciente__apellidos__icontains=q) |
            Q(doctor__apellidos__icontains=q)
        )
    if estado:
        qs = qs.filter(estado=estado)
    if fecha:
        qs = qs.filter(fecha_hora__date=fecha)

    paginator = Paginator(qs, 20)
    citas = paginator.get_page(request.GET.get('page'))
    return render(request, 'citas/lista.html', {'citas': citas, 'rol': rol})


# ── Crear cita ─────────────────────────────────────────────────
@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def crear(request):
    from apps.pacientes.models import Paciente
    from datetime import datetime
    pacientes      = Paciente.objects.filter(activo=True).order_by('apellidos')
    especialidades = Doctor.objects.filter(activo=True).values_list(
        'especialidad', flat=True
    ).distinct().order_by('especialidad')

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            nueva = form.save(commit=False)

            # ── Validar solapamiento en backend ──────────────────
            error_solapamiento = _validar_solapamiento(nueva, excluir_pk=None)
            if error_solapamiento:
                messages.error(request, error_solapamiento)
            else:
                nueva.save()
                messages.success(request, 'Cita registrada correctamente.')
                return redirect('citas:lista')
    else:
        form = CitaForm()
        if request.GET.get('paciente'):
            form.initial['paciente'] = request.GET.get('paciente')

    return render(request, 'citas/form.html', {
        'form':           form,
        'pacientes':      pacientes,
        'especialidades': list(especialidades),
        'hoy':            date.today().isoformat(),
    })


# ── Editar cita ────────────────────────────────────────────────
@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def editar(request, pk):
    from apps.pacientes.models import Paciente
    cita      = get_object_or_404(Cita, pk=pk)
    pacientes = Paciente.objects.filter(activo=True).order_by('apellidos')
    doctores  = Doctor.objects.filter(activo=True).order_by('apellidos')
    especialidades = Doctor.objects.filter(activo=True).values_list(
        'especialidad', flat=True
    ).distinct().order_by('especialidad')

    form = CitaForm(request.POST or None, instance=cita)
    if request.method == 'POST' and form.is_valid():
        editada = form.save(commit=False)
        error_solapamiento = _validar_solapamiento(editada, excluir_pk=cita.pk)
        if error_solapamiento:
            messages.error(request, error_solapamiento)
        else:
            editada.save()
            messages.success(request, 'Cita actualizada.')
            return redirect('citas:lista')

    return render(request, 'citas/form.html', {
        'form':           form,
        'cita':           cita,
        'pacientes':      pacientes,
        'doctores':       doctores,
        'especialidades': list(especialidades),
        'hoy':            date.today().isoformat(),
    })


# ── Eliminar cita ──────────────────────────────────────────────
@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def eliminar(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada.')
    return redirect('citas:lista')


# ── Cambiar estado ─────────────────────────────────────────────
@login_required
def cambiar_estado(request, pk):
    rol  = get_rol(request.user)
    cita = get_object_or_404(Cita, pk=pk)

    if rol == 'DOCTOR' and cita.doctor.usuario != request.user:
        messages.error(request, 'No tienes permiso.')
        return redirect('citas:lista')

    estado = request.GET.get('estado')
    if estado in ['PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA', 'NO_ASISTIO']:
        cita.estado = estado
        cita.save(update_fields=['estado'])
        messages.success(request, f'Estado: {cita.get_estado_display()}')
    return redirect('citas:lista')