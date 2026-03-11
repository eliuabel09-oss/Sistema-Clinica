# apps/core/views_dashboard.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from apps.pacientes.models import Paciente
from apps.citas.models import Cita
from apps.core.decorators import get_rol


@login_required
def dashboard(request):
    rol = get_rol(request.user)

    # FIX: doctor va directo a su perfil
    if rol == 'DOCTOR':
        return redirect('doctores:mi_perfil')

    hoy = timezone.localdate()

    # Stats principales
    total_pacientes  = Paciente.objects.filter(activo=True).count()
    citas_hoy        = Cita.objects.filter(fecha_hora__date=hoy).count()
    citas_pendientes = Cita.objects.filter(estado='PENDIENTE').count()

    # Próximas citas
    proximas_citas = (
        Cita.objects
        .filter(fecha_hora__date__gte=hoy, estado__in=['PENDIENTE', 'CONFIRMADA'])
        .select_related('paciente', 'doctor')
        .order_by('fecha_hora')[:10]
    )

    # Últimos pacientes
    ultimos_pacientes = Paciente.objects.filter(activo=True).order_by('-id')[:5]

    # Gráfica semanal — Lunes de esta semana
    lunes = hoy - timedelta(days=hoy.weekday())
    dias_semana = []
    nombres_cortos = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

    citas_semana_total       = 0
    citas_completadas_semana = 0
    citas_confirmadas_semana = 0
    citas_pendientes_semana  = 0
    citas_canceladas_semana  = 0

    for i in range(7):
        fecha    = lunes + timedelta(days=i)
        citas_d  = Cita.objects.filter(fecha_hora__date=fecha)
        total_d  = citas_d.count()

        citas_semana_total       += total_d
        citas_completadas_semana += citas_d.filter(estado='COMPLETADA').count()
        citas_confirmadas_semana += citas_d.filter(estado='CONFIRMADA').count()
        citas_pendientes_semana  += citas_d.filter(estado='PENDIENTE').count()
        citas_canceladas_semana  += citas_d.filter(estado='CANCELADA').count()

        dias_semana.append({
            'fecha':     fecha,
            'dia_corto': nombres_cortos[i],
            'total':     total_d,
            'es_hoy':    fecha == hoy,
        })

    return render(request, 'dashboard.html', {
        'total_pacientes':  total_pacientes,
        'citas_hoy':        citas_hoy,
        'citas_pendientes': citas_pendientes,
        'proximas_citas':   proximas_citas,
        'ultimos_pacientes': ultimos_pacientes,
        # Gráfica
        'citas_semana':              dias_semana,
        'citas_semana_total':        citas_semana_total,
        'citas_completadas_semana':  citas_completadas_semana,
        'citas_confirmadas_semana':  citas_confirmadas_semana,
        'citas_pendientes_semana':   citas_pendientes_semana,
        'citas_canceladas_semana':   citas_canceladas_semana,
    })