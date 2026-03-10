# apps/core/views_dashboard.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.core.decorators import get_rol


@login_required
def dashboard(request):
    from apps.pacientes.models import Paciente
    from apps.citas.models import Cita
    from apps.consultas.models import Consulta

    rol = get_rol(request.user)
    hoy = timezone.now().date()

    # Doctor → redirigir directo a su perfil
    if rol == 'DOCTOR':
        return redirect('doctores:mi_perfil')

    context = {
        'total_pacientes':   Paciente.objects.filter(activo=True).count(),
        'citas_hoy':         Cita.objects.filter(fecha_hora__date=hoy).count(),
        'citas_pendientes':  Cita.objects.filter(estado='PENDIENTE').count(),
        'total_consultas':   Consulta.objects.filter(
                                 fecha__month=hoy.month,
                                 fecha__year=hoy.year
                             ).count(),
        'proximas_citas':    Cita.objects.filter(
                                 fecha_hora__gte=timezone.now()
                             ).select_related('paciente', 'doctor').order_by('fecha_hora')[:8],
        'ultimos_pacientes': Paciente.objects.order_by('-fecha_registro')[:5],
        'rol': rol,
    }
    return render(request, 'dashboard.html', context)