# apps/core/views_dashboard.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime
from apps.pacientes.models import Paciente
from apps.citas.models import Cita
from apps.core.decorators import get_rol


def _rango_local(fecha_inicio, fecha_fin):
    """Convierte fechas locales a datetimes aware para filtrar correctamente con USE_TZ=True."""
    ini = timezone.make_aware(datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day, 0, 0, 0))
    fin = timezone.make_aware(datetime(fecha_fin.year,    fecha_fin.month,    fecha_fin.day,    23, 59, 59))
    return ini, fin


@login_required
def dashboard(request):
    rol = get_rol(request.user)

    if rol == 'DOCTOR':
        return redirect('doctores:mi_perfil')

    hoy   = timezone.localdate()
    ahora = timezone.localtime()

    # ── Filtro de periodo ─────────────────────────────────────
    periodo = request.GET.get('periodo', 'semana')   # dia | semana | mes | anio

    if periodo == 'dia':
        fecha_ini = hoy
        fecha_fin = hoy
        titulo_periodo = f'Hoy — {hoy.strftime("%d/%m/%Y")}'
        # Gráfica: 24 horas del día (bloques de 2h)
        etiquetas_grafica = [f'{h:02d}h' for h in range(0, 24, 2)]
        def citas_grafica():
            resultado = []
            for h in range(0, 24, 2):
                ini = timezone.make_aware(datetime(hoy.year, hoy.month, hoy.day, h, 0, 0))
                fin = timezone.make_aware(datetime(hoy.year, hoy.month, hoy.day, min(h+1, 23), 59, 59))
                total = Cita.objects.filter(fecha_hora__gte=ini, fecha_hora__lte=fin).count()
                resultado.append({'etiqueta': f'{h:02d}h', 'total': total, 'es_hoy': True})
            return resultado

    elif periodo == 'mes':
        fecha_ini = hoy.replace(day=1)
        import calendar
        ultimo_dia = calendar.monthrange(hoy.year, hoy.month)[1]
        fecha_fin  = hoy.replace(day=ultimo_dia)
        titulo_periodo = hoy.strftime('%B %Y').capitalize()
        # Gráfica: semanas del mes
        etiquetas_grafica = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5']
        def citas_grafica():
            resultado = []
            for semana in range(5):
                d_ini = fecha_ini + timedelta(weeks=semana)
                d_fin = min(d_ini + timedelta(days=6), fecha_fin)
                if d_ini > fecha_fin:
                    break
                ini, fin = _rango_local(d_ini, d_fin)
                total = Cita.objects.filter(fecha_hora__gte=ini, fecha_hora__lte=fin).count()
                resultado.append({'etiqueta': f'S{semana+1}', 'total': total, 'es_hoy': False})
            return resultado

    elif periodo == 'anio':
        fecha_ini = hoy.replace(month=1, day=1)
        fecha_fin = hoy.replace(month=12, day=31)
        titulo_periodo = str(hoy.year)
        nombres_meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
        def citas_grafica():
            import calendar
            resultado = []
            for mes in range(1, 13):
                ultimo = calendar.monthrange(hoy.year, mes)[1]
                d_ini  = hoy.replace(month=mes, day=1)
                d_fin  = hoy.replace(month=mes, day=ultimo)
                ini, fin = _rango_local(d_ini, d_fin)
                total  = Cita.objects.filter(fecha_hora__gte=ini, fecha_hora__lte=fin).count()
                resultado.append({
                    'etiqueta': nombres_meses[mes-1],
                    'total':    total,
                    'es_hoy':   mes == hoy.month,
                })
            return resultado

    else:  # semana (default)
        periodo    = 'semana'
        lunes      = hoy - timedelta(days=hoy.weekday())
        fecha_ini  = lunes
        fecha_fin  = lunes + timedelta(days=6)
        titulo_periodo = f'{lunes.strftime("%d %b")} – {fecha_fin.strftime("%d %b %Y")}'
        nombres_cortos = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        def citas_grafica():
            resultado = []
            for i in range(7):
                fecha = lunes + timedelta(days=i)
                ini, fin = _rango_local(fecha, fecha)
                total = Cita.objects.filter(fecha_hora__gte=ini, fecha_hora__lte=fin).count()
                resultado.append({
                    'etiqueta': nombres_cortos[i],
                    'total':    total,
                    'es_hoy':   fecha == hoy,
                })
            return resultado

    # ── Rango del periodo seleccionado ───────────────────────
    ini_periodo, fin_periodo = _rango_local(fecha_ini, fecha_fin)

    citas_periodo = Cita.objects.filter(
        fecha_hora__gte=ini_periodo,
        fecha_hora__lte=fin_periodo,
    )

    # ── Stats del periodo ─────────────────────────────────────
    total_pacientes   = Paciente.objects.filter(activo=True).count()

    ini_hoy, fin_hoy  = _rango_local(hoy, hoy)
    citas_hoy_count   = Cita.objects.filter(fecha_hora__gte=ini_hoy, fecha_hora__lte=fin_hoy).count()
    citas_pendientes  = Cita.objects.filter(estado='PENDIENTE').count()

    total_periodo        = citas_periodo.count()
    completadas_periodo  = citas_periodo.filter(estado='COMPLETADA').count()
    confirmadas_periodo  = citas_periodo.filter(estado='CONFIRMADA').count()
    pendientes_periodo   = citas_periodo.filter(estado='PENDIENTE').count()
    canceladas_periodo   = citas_periodo.filter(estado='CANCELADA').count()

    # ── Gráfica ───────────────────────────────────────────────
    datos_grafica = citas_grafica()

    # ── Próximas citas ────────────────────────────────────────
    proximas_citas = (
        Cita.objects
        .filter(fecha_hora__gte=ahora, estado__in=['PENDIENTE', 'CONFIRMADA'])
        .select_related('paciente', 'doctor')
        .order_by('fecha_hora')[:10]
    )

    # ── Últimos pacientes ─────────────────────────────────────
    ultimos_pacientes = Paciente.objects.filter(activo=True).order_by('-id')[:5]

    return render(request, 'dashboard.html', {
        'rol':              rol,
        'periodo':          periodo,
        'titulo_periodo':   titulo_periodo,
        # Stats globales
        'total_pacientes':  total_pacientes,
        'citas_hoy':        citas_hoy_count,
        'citas_pendientes': citas_pendientes,
        # Stats del periodo
        'total_periodo':       total_periodo,
        'completadas_periodo': completadas_periodo,
        'confirmadas_periodo': confirmadas_periodo,
        'pendientes_periodo':  pendientes_periodo,
        'canceladas_periodo':  canceladas_periodo,
        # Gráfica
        'datos_grafica':    datos_grafica,
        # Tablas
        'proximas_citas':    proximas_citas,
        'ultimos_pacientes': ultimos_pacientes,
        'hoy':              hoy,
    })
