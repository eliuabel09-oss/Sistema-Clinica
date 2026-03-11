# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# FIX: usar views_dashboard en lugar de la función inline
from apps.core.views_dashboard import dashboard

urlpatterns = [
    path('admin/',     admin.site.urls),
    path('',           dashboard,  name='dashboard'),

    # Auth
    path('login/',     auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/',    auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Módulos
    path('pacientes/', include('apps.pacientes.urls',      namespace='pacientes')),
    path('citas/',     include('apps.citas.urls',          namespace='citas')),
    path('consultas/', include('apps.consultas.urls',      namespace='consultas')),
    path('doctores/',  include('apps.citas.urls_doctores', namespace='doctores')),
    path('usuarios/',  include('apps.core.urls_usuarios',  namespace='usuarios')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)