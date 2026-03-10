# config/urls.py — VERSIÓN COMPLETA FINAL
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone


@login_required
def dashboard(request):
    from apps.pacientes.models import Paciente
    from apps.citas.models import Cita
    from apps.consultas.models import Consulta
    from apps.core.decorators import get_rol

    rol = get_rol(request.user)
    hoy = timezone.now().date()

    # Si es doctor → redirigir a su perfil directamente
    if rol == 'DOCTOR':
        return redirect('doctores:mi_perfil')

    context = {
        'total_pacientes':   Paciente.objects.filter(activo=True).count(),
        'citas_hoy':         Cita.objects.filter(fecha_hora__date=hoy).count(),
        'citas_pendientes':  Cita.objects.filter(estado='PENDIENTE').count(),
        'total_consultas':   Consulta.objects.filter(fecha__month=hoy.month, fecha__year=hoy.year).count(),
        'proximas_citas':    Cita.objects.filter(fecha_hora__gte=timezone.now()).select_related('paciente', 'doctor').order_by('fecha_hora')[:8],
        'ultimos_pacientes': Paciente.objects.order_by('-fecha_registro')[:5],
        'rol': rol,
    }
    return render(request, 'dashboard.html', context)


urlpatterns = [
    path('admin/',     admin.site.urls),
    path('',           dashboard,  name='dashboard'),

    # Auth
    path('login/',     auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/',    auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Módulos
    path('pacientes/', include('apps.pacientes.urls',          namespace='pacientes')),
    path('citas/',     include('apps.citas.urls',              namespace='citas')),
    path('consultas/', include('apps.consultas.urls',          namespace='consultas')),
    path('doctores/',  include('apps.citas.urls_doctores',     namespace='doctores')),
    path('usuarios/',  include('apps.core.urls_usuarios',      namespace='usuarios')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)