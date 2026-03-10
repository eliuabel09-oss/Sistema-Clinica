# apps/pacientes/views.py — ACTUALIZADO CON ROLES
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from apps.core.decorators import rol_requerido, get_rol
from .models import Paciente, ArchivoClinico
from .forms import PacienteForm, ArchivoClinicoForm


@login_required
def lista(request):
    rol = get_rol(request.user)

    if rol == 'DOCTOR':
        # El doctor solo ve sus pacientes (los que ha atendido)
        from apps.citas.models import Cita
        ids = Cita.objects.filter(doctor__usuario=request.user).values_list('paciente_id', flat=True).distinct()
        qs = Paciente.objects.filter(pk__in=ids)
    else:
        qs = Paciente.objects.all()

    q    = request.GET.get('q', '').strip()
    sexo = request.GET.get('sexo', '')
    if q:
        qs = qs.filter(Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(curp__icontains=q))
    if sexo:
        qs = qs.filter(sexo=sexo)

    paginator = Paginator(qs, 20)
    pacientes = paginator.get_page(request.GET.get('page'))
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes, 'total': qs.count()})


@login_required
def detalle(request, pk):
    paciente  = get_object_or_404(Paciente, pk=pk)
    citas     = paciente.citas.select_related('doctor').order_by('-fecha_hora')[:10]
    consultas = paciente.consultas.select_related('doctor').prefetch_related('recetas').order_by('-fecha')[:10]
    return render(request, 'pacientes/detalle.html', {
        'paciente': paciente, 'citas': citas, 'consultas': consultas
    })


@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def crear(request):
    form = PacienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        paciente = form.save()
        messages.success(request, f'Paciente {paciente.nombre_completo} registrado.')
        return redirect('pacientes:detalle', pk=paciente.pk)
    return render(request, 'pacientes/form.html', {'form': form})


@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def editar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    form = PacienteForm(request.POST or None, instance=paciente)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Datos actualizados.')
        return redirect('pacientes:detalle', pk=pk)
    return render(request, 'pacientes/form.html', {'form': form, 'paciente': paciente})


@login_required
@rol_requerido('ADMIN')
def eliminar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        nombre = paciente.nombre_completo
        paciente.delete()
        messages.success(request, f'Paciente {nombre} eliminado.')
        return redirect('pacientes:lista')
    return redirect('pacientes:detalle', pk=pk)


@login_required
@rol_requerido('ADMIN', 'SECRETARIA')
def subir_archivo(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = ArchivoClinicoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.paciente = paciente
            archivo.save()
            messages.success(request, 'Archivo subido.')
            return redirect('pacientes:detalle', pk=pk)
    else:
        form = ArchivoClinicoForm()
    return render(request, 'pacientes/subir_archivo.html', {'form': form, 'paciente': paciente})