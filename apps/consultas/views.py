# apps/consultas/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from apps.core.decorators import rol_requerido, get_rol
from .models import Consulta, Receta
from apps.pacientes.models import Paciente
from apps.citas.models import Cita, Doctor


@login_required
def lista(request):
    rol = get_rol(request.user)

    if rol == 'DOCTOR':
        qs = Consulta.objects.filter(doctor__usuario=request.user)
    else:
        qs = Consulta.objects.all()

    qs = qs.select_related('paciente', 'doctor').prefetch_related('recetas').order_by('-fecha')

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

    paginator = Paginator(qs, 20)
    consultas = paginator.get_page(request.GET.get('page'))
    doctores  = Doctor.objects.filter(activo=True).order_by('apellidos')
    return render(request, 'consultas/lista.html', {
        'consultas': consultas,
        'doctores':  doctores,
        'rol':       rol,
    })


@login_required
def detalle(request, pk):
    consulta = get_object_or_404(
        Consulta.objects.select_related('paciente', 'doctor').prefetch_related('recetas'),
        pk=pk
    )
    rol = get_rol(request.user)

    if rol == 'DOCTOR' and consulta.doctor.usuario != request.user:
        messages.error(request, 'No tienes permiso para ver esta consulta.')
        return redirect('consultas:lista')

    soap_fields = [
        ('S — Subjetivo',   '#0369a1', consulta.subjetivo),
        ('O — Objetivo',    '#0d9488', consulta.objetivo),
        ('A — Diagnóstico', '#7c3aed', consulta.diagnostico),
        ('P — Plan',        '#d97706', consulta.plan),
    ]
    if consulta.evolucion:
        soap_fields.append(('Evolución', '#475569', consulta.evolucion))

    return render(request, 'consultas/detalle.html', {
        'consulta':    consulta,
        'soap_fields': soap_fields,
        'rol':         rol,
    })


@login_required
@rol_requerido('ADMIN', 'SECRETARIA', 'DOCTOR')
def crear(request):
    rol = get_rol(request.user)

    pacientes = Paciente.objects.filter(activo=True).order_by('apellidos')
    doctores  = Doctor.objects.filter(activo=True).order_by('apellidos')

    doctor_actual = None
    if rol == 'DOCTOR':
        doctor_actual = Doctor.objects.filter(usuario=request.user).first()

    cita_preseleccionada = None
    cita_id_get = request.GET.get('cita')
    if cita_id_get:
        try:
            cita_preseleccionada = Cita.objects.select_related(
                'paciente', 'doctor'
            ).get(pk=cita_id_get)
            if rol == 'DOCTOR' and doctor_actual and cita_preseleccionada.doctor != doctor_actual:
                messages.error(request, 'No tienes permiso para registrar consulta en esa cita.')
                return redirect('doctores:mi_perfil')
            if hasattr(cita_preseleccionada, 'consulta'):
                messages.warning(
                    request,
                    f'La cita del {cita_preseleccionada.fecha_hora.strftime("%d/%m/%Y %H:%M")} '
                    f'con {cita_preseleccionada.paciente.nombre_completo} '
                    f'ya tiene una consulta registrada.'
                )
                if rol == 'DOCTOR':
                    return redirect('doctores:mi_perfil')
                return redirect('consultas:detalle', pk=cita_preseleccionada.consulta.pk)
        except Cita.DoesNotExist:
            cita_preseleccionada = None

    if rol == 'DOCTOR':
        citas_disponibles = Cita.objects.filter(
            doctor__usuario=request.user,
            estado__in=['CONFIRMADA', 'PENDIENTE']
        ).select_related('paciente').order_by('-fecha_hora')[:50]
    else:
        citas_disponibles = Cita.objects.filter(
            estado__in=['CONFIRMADA', 'PENDIENTE']
        ).select_related('paciente').order_by('-fecha_hora')[:50]

    if request.method == 'POST':
        # FIX: todo dentro de transaction.atomic para evitar datos parciales
        try:
            with transaction.atomic():
                doctor_id = request.POST.get('doctor')
                if rol == 'DOCTOR' and doctor_actual:
                    doctor_id = doctor_actual.pk

                # Validar cita no duplicada
                cita_post_id = request.POST.get('cita') or None
                if cita_post_id:
                    try:
                        cita_obj = Cita.objects.get(pk=cita_post_id)
                        if hasattr(cita_obj, 'consulta'):
                            messages.error(
                                request,
                                f'La cita del {cita_obj.fecha_hora.strftime("%d/%m/%Y %H:%M")} '
                                f'ya tiene una consulta registrada. No se puede duplicar.'
                            )
                            if rol == 'DOCTOR':
                                return redirect('doctores:mi_perfil')
                            return redirect('consultas:lista')
                    except Cita.DoesNotExist:
                        cita_post_id = None

                # Validar campos obligatorios
                paciente_id = request.POST.get('paciente')
                if not paciente_id or not doctor_id:
                    messages.error(request, 'Paciente y doctor son obligatorios.')
                    raise ValueError('Campos obligatorios faltantes')

                consulta = Consulta.objects.create(
                    paciente_id         = paciente_id,
                    doctor_id           = doctor_id,
                    cita_id             = cita_post_id,
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

                # Guardar recetas — dentro de la misma transacción
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
                            dosis       = dosis_list[i]   if i < len(dosis_list)   else '',
                            frecuencia  = frecuencias[i]  if i < len(frecuencias)  else '',
                            duracion    = duraciones[i]   if i < len(duraciones)   else '',
                            indicaciones= indicaciones[i] if i < len(indicaciones) else '',
                            orden       = i + 1,
                        )

                # Marcar cita completada — dentro de la misma transacción
                if consulta.cita:
                    consulta.cita.estado = 'COMPLETADA'
                    consulta.cita.save(update_fields=['estado'])

                messages.success(request, 'Consulta registrada correctamente.')

                if rol == 'DOCTOR':
                    return redirect('doctores:mi_perfil')
                return redirect('consultas:detalle', pk=consulta.pk)

        except ValueError:
            pass  # ya manejado con messages.error
        except Exception as e:
            messages.error(request, f'Error al guardar la consulta: {e}')

    return render(request, 'consultas/form.html', {
        'pacientes':            pacientes,
        'doctores':             doctores,
        'citas_disponibles':    citas_disponibles,
        'cita_preseleccionada': cita_preseleccionada,
        'doctor_actual':        doctor_actual,
        'rol':                  rol,
        'hoy_iso':              timezone.now().date().isoformat(),
    })


@login_required
@rol_requerido('ADMIN')
def eliminar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        # FIX: si la cita quedó COMPLETADA por esta consulta, revertir a CONFIRMADA
        if consulta.cita and consulta.cita.estado == 'COMPLETADA':
            consulta.cita.estado = 'CONFIRMADA'
            consulta.cita.save(update_fields=['estado'])
        consulta.delete()
        messages.success(request, 'Consulta eliminada.')
    return redirect('consultas:lista')