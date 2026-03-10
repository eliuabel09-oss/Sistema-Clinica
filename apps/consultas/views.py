# apps/consultas/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Consulta, Receta
from apps.pacientes.models import Paciente
from apps.citas.models import Cita, Doctor


def lista(request):
    qs = Consulta.objects.select_related('paciente', 'doctor').prefetch_related('recetas').order_by('-fecha')
    q      = request.GET.get('q', '').strip()
    doctor = request.GET.get('doctor', '')
    if q:
        qs = qs.filter(
            Q(paciente__nombres__icontains=q) |
            Q(paciente__apellidos__icontains=q) |
            Q(diagnostico__icontains=q) |
            Q(doctor__apellidos__icontains=q)
        )
    if doctor:
        qs = qs.filter(doctor_id=doctor)
    doctores = Doctor.objects.filter(activo=True).order_by('apellidos')
    return render(request, 'consultas/lista.html', {'consultas': qs, 'doctores': doctores})


def detalle(request, pk):
    consulta = get_object_or_404(Consulta.objects.select_related('paciente', 'doctor').prefetch_related('recetas'), pk=pk)
    soap_fields = [
        ('S — Subjetivo',  '#0369a1', consulta.subjetivo),
        ('O — Objetivo',   '#0d9488', consulta.objetivo),
        ('A — Diagnóstico','#7c3aed', consulta.diagnostico),
        ('P — Plan',       '#d97706', consulta.plan),
    ]
    if consulta.evolucion:
        soap_fields.append(('Evolución', '#475569', consulta.evolucion))
    return render(request, 'consultas/detalle.html', {'consulta': consulta, 'soap_fields': soap_fields})


def crear(request):
    pacientes        = Paciente.objects.filter(activo=True).order_by('apellidos')
    doctores         = Doctor.objects.filter(activo=True).order_by('apellidos')
    citas_disponibles = Cita.objects.filter(estado__in=['CONFIRMADA', 'PENDIENTE']).select_related('paciente').order_by('-fecha_hora')[:50]

    if request.method == 'POST':
        try:
            consulta = Consulta.objects.create(
                paciente_id         = request.POST.get('paciente'),
                doctor_id           = request.POST.get('doctor'),
                cita_id             = request.POST.get('cita') or None,
                peso_kg             = request.POST.get('peso_kg')             or None,
                talla_cm            = request.POST.get('talla_cm')            or None,
                temperatura         = request.POST.get('temperatura')         or None,
                presion_arterial    = request.POST.get('presion_arterial',    ''),
                frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca') or None,
                saturacion_o2       = request.POST.get('saturacion_o2')       or None,
                subjetivo           = request.POST.get('subjetivo',   ''),
                objetivo            = request.POST.get('objetivo',    ''),
                diagnostico         = request.POST.get('diagnostico', ''),
                plan                = request.POST.get('plan',        ''),
                evolucion           = request.POST.get('evolucion',   ''),
                proxima_cita        = request.POST.get('proxima_cita') or None,
            )
            # Guardar recetas
            medicamentos = request.POST.getlist('medicamento[]')
            dosis_list   = request.POST.getlist('dosis[]')
            frecuencias  = request.POST.getlist('frecuencia[]')
            duraciones   = request.POST.getlist('duracion[]')
            indicaciones = request.POST.getlist('indicaciones[]')

            for i, med in enumerate(medicamentos):
                if med.strip():
                    Receta.objects.create(
                        consulta    = consulta,
                        medicamento = med.strip(),
                        dosis       = dosis_list[i]  if i < len(dosis_list)  else '',
                        frecuencia  = frecuencias[i] if i < len(frecuencias) else '',
                        duracion    = duraciones[i]  if i < len(duraciones)  else '',
                        indicaciones= indicaciones[i]if i < len(indicaciones)else '',
                        orden       = i + 1,
                    )

            # Marcar cita como completada si estaba asociada
            if consulta.cita:
                consulta.cita.estado = 'COMPLETADA'
                consulta.cita.save(update_fields=['estado'])

            messages.success(request, 'Consulta registrada correctamente.')
            return redirect('consultas:detalle', pk=consulta.pk)

        except Exception as e:
            messages.error(request, f'Error al guardar la consulta: {e}')

    from django import forms as dj_forms
    class FakeForm:
        def __getattr__(self, name):
            class V:
                value = lambda s: ''
            return V()
    return render(request, 'consultas/form.html', {
        'form': FakeForm(),
        'pacientes': pacientes,
        'doctores': doctores,
        'citas_disponibles': citas_disponibles,
    })