# apps/citas/views_doctores.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.core.decorators import rol_requerido
from apps.core.models import PerfilUsuario
from .models import Doctor, Cita, HorarioDoctor
from .forms_doctores import DoctorForm, DoctorUsuarioForm


DIAS_SEMANA = [
    (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'),
    (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo'),
]


def _guardar_horarios_doctor(doctor, post_data):
    """Guarda los horarios del doctor desde los datos del formulario."""
    HorarioDoctor.objects.filter(doctor=doctor).delete()
    for dia_num, _ in DIAS_SEMANA:
        activo   = post_data.get(f'dia_{dia_num}')
        hora_ini = post_data.get(f'ini_{dia_num}')
        hora_fin = post_data.get(f'fin_{dia_num}')
        if activo and hora_ini and hora_fin:
            try:
                HorarioDoctor.objects.create(
                    doctor=doctor,
                    dia_semana=dia_num,
                    hora_inicio=hora_ini,
                    hora_fin=hora_fin,
                )
            except Exception:
                pass


def _asignar_rol_doctor(user):
    """Garantiza que el perfil del usuario tenga rol DOCTOR."""
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=user)
    perfil.rol = 'DOCTOR'
    perfil.save()


# ── Lista de doctores (solo Admin) ─────────────────────────────
@login_required
@rol_requerido('ADMIN')
def lista(request):
    doctores = Doctor.objects.select_related('usuario').order_by('apellidos')
    return render(request, 'doctores/lista.html', {'doctores': doctores})


# ── Crear doctor + opcionalmente su usuario ────────────────────
@login_required
@rol_requerido('ADMIN')
def crear(request):
    form         = DoctorForm(request.POST or None, request.FILES or None)
    form_usuario = DoctorUsuarioForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        doctor = form.save(commit=False)

        crear_user = request.POST.get('crear_usuario')
        if crear_user and form_usuario.is_valid():
            username  = form_usuario.cleaned_data['username']
            password  = form_usuario.cleaned_data['password1']
            user = User.objects.create_user(
                username   = username,
                password   = password,
                first_name = doctor.nombres,
                last_name  = doctor.apellidos,
                email      = doctor.email,
            )
            _asignar_rol_doctor(user)
            doctor.usuario = user

        doctor.save()
        _guardar_horarios_doctor(doctor, request.POST)
        messages.success(request, f'Dr. {doctor.apellidos} registrado correctamente.')
        return redirect('doctores:lista')

    return render(request, 'doctores/form.html', {
        'form':              form,
        'form_usuario':      form_usuario,
        'dias_semana':       DIAS_SEMANA,
        'horarios_actuales': {},
    })


# ── Editar doctor ──────────────────────────────────────────────
@login_required
@rol_requerido('ADMIN')
def editar(request, pk):
    doctor       = get_object_or_404(Doctor, pk=pk)
    form         = DoctorForm(request.POST or None, request.FILES or None, instance=doctor)
    form_usuario = DoctorUsuarioForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        doctor = form.save(commit=False)

        crear_user = request.POST.get('crear_usuario')
        if crear_user and not doctor.usuario and form_usuario.is_valid():
            username = form_usuario.cleaned_data['username']
            password = form_usuario.cleaned_data['password1']
            user = User.objects.create_user(
                username   = username,
                password   = password,
                first_name = doctor.nombres,
                last_name  = doctor.apellidos,
                email      = doctor.email,
            )
            _asignar_rol_doctor(user)
            doctor.usuario = user

        doctor.save()
        _guardar_horarios_doctor(doctor, request.POST)
        messages.success(request, 'Doctor actualizado correctamente.')
        return redirect('doctores:lista')

    horarios_actuales = {
        h.dia_semana: h
        for h in HorarioDoctor.objects.filter(doctor=doctor)
    }
    return render(request, 'doctores/form.html', {
        'form':              form,
        'form_usuario':      form_usuario,
        'doctor':            doctor,
        'dias_semana':       DIAS_SEMANA,
        'horarios_actuales': horarios_actuales,
    })


# ── Eliminar doctor ────────────────────────────────────────────
@login_required
@rol_requerido('ADMIN')
def eliminar(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        nombre = doctor.apellidos
        if doctor.usuario:
            doctor.usuario.delete()
        else:
            doctor.delete()
        messages.success(request, f'Dr. {nombre} eliminado.')
    return redirect('doctores:lista')


# ── Perfil del doctor ──────────────────────────────────────────
@login_required
@rol_requerido('DOCTOR')
def mi_perfil(request):
    doctor = get_object_or_404(Doctor, usuario=request.user)

    total_citas       = doctor.citas.count()
    citas_completadas = doctor.citas.filter(estado='COMPLETADA').count()
    citas_hoy         = doctor.citas.filter(fecha_hora__date=timezone.now().date()).count()
    proximas_citas    = doctor.citas.filter(
        fecha_hora__gte=timezone.now(),
        estado__in=['PENDIENTE', 'CONFIRMADA']
    ).select_related('paciente').order_by('fecha_hora')[:10]

    from apps.pacientes.models import Paciente
    pacientes_ids       = doctor.citas.filter(estado='COMPLETADA').values_list('paciente_id', flat=True).distinct()
    pacientes_atendidos = Paciente.objects.filter(pk__in=pacientes_ids)
    citas_recientes     = doctor.citas.select_related('paciente').order_by('-fecha_hora')[:15]

    return render(request, 'doctores/mi_perfil.html', {
        'doctor':               doctor,
        'total_citas':          total_citas,
        'citas_completadas':    citas_completadas,
        'citas_hoy':            citas_hoy,
        'proximas_citas':       proximas_citas,
        'pacientes_atendidos':  pacientes_atendidos,
        'citas_recientes':      citas_recientes,
    })


# ── Informe del doctor en una cita ────────────────────────────
@login_required
@rol_requerido('DOCTOR')
def escribir_informe(request, cita_pk):
    doctor = get_object_or_404(Doctor, usuario=request.user)
    cita   = get_object_or_404(Cita, pk=cita_pk, doctor=doctor)

    if request.method == 'POST':
        cita.informe_doctor = request.POST.get('informe_doctor', '')
        cita.informe_fecha  = timezone.now()
        cita.save(update_fields=['informe_doctor', 'informe_fecha'])
        messages.success(request, 'Informe guardado correctamente.')
        return redirect('doctores:mi_perfil')

    return render(request, 'doctores/informe.html', {'cita': cita, 'doctor': doctor})


# ── Editar horarios del doctor (Admin) ────────────────────────
@login_required
@rol_requerido('ADMIN')
def editar_horarios(request, pk):
    """Configura los días y horas en que un doctor atiende."""
    doctor = get_object_or_404(Doctor, pk=pk)

    DIAS = [
        (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'),
        (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo'),
    ]

    if request.method == 'POST':
        _guardar_horarios_doctor(doctor, request.POST)
        messages.success(request, f'Horarios de Dr. {doctor.apellidos} actualizados.')
        return redirect('doctores:lista')

    horarios_actuales = {
        h.dia_semana: h
        for h in HorarioDoctor.objects.filter(doctor=doctor)
    }

    return render(request, 'doctores/horarios.html', {
        'doctor':            doctor,
        'dias':              DIAS,
        'horarios_actuales': horarios_actuales,
    })
