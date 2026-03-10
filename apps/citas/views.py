# apps/citas/views.py — ACTUALIZADO CON ROLES
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from apps.core.decorators import rol_requerido, get_rol
from .models import Cita, Doctor
from .forms import CitaForm


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


@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def crear(request):
    from apps.pacientes.models import Paciente
    form      = CitaForm(request.POST or None)
    pacientes = Paciente.objects.filter(activo=True).order_by('apellidos')
    doctores  = Doctor.objects.filter(activo=True).order_by('apellidos')
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cita registrada.')
        return redirect('citas:lista')
    return render(request, 'citas/form.html', {
        'form': form, 'pacientes': pacientes, 'doctores': doctores
    })


@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def editar(request, pk):
    from apps.pacientes.models import Paciente
    cita      = get_object_or_404(Cita, pk=pk)
    form      = CitaForm(request.POST or None, instance=cita)
    pacientes = Paciente.objects.filter(activo=True).order_by('apellidos')
    doctores  = Doctor.objects.filter(activo=True).order_by('apellidos')
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cita actualizada.')
        return redirect('citas:lista')
    return render(request, 'citas/form.html', {
        'form': form, 'cita': cita, 'pacientes': pacientes, 'doctores': doctores
    })


@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def eliminar(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada.')
    return redirect('citas:lista')


@login_required
def cambiar_estado(request, pk):
    rol  = get_rol(request.user)
    cita = get_object_or_404(Cita, pk=pk)

    # El doctor solo puede cambiar estado de sus propias citas
    if rol == 'DOCTOR' and cita.doctor.usuario != request.user:
        messages.error(request, 'No tienes permiso.')
        return redirect('citas:lista')

    estado = request.GET.get('estado')
    if estado in ['PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA', 'NO_ASISTIO']:
        cita.estado = estado
        cita.save(update_fields=['estado'])
        messages.success(request, f'Estado: {cita.get_estado_display()}')
    return redirect('citas:lista')