# apps/citas/urls_doctores.py — VERSIÓN ACTUALIZADA
# Agrega la ruta de horarios al final
from django.urls import path
from . import views_doctores

app_name = 'doctores'

urlpatterns = [
    path('',                          views_doctores.lista,          name='lista'),
    path('nuevo/',                    views_doctores.crear,          name='crear'),
    path('<int:pk>/editar/',          views_doctores.editar,         name='editar'),
    path('<int:pk>/eliminar/',        views_doctores.eliminar,       name='eliminar'),
    path('mi-perfil/',                views_doctores.mi_perfil,      name='mi_perfil'),
    path('informe/<int:cita_pk>/',    views_doctores.escribir_informe, name='informe'),

    # ── NUEVO: gestión de horarios del doctor ──
    path('<int:pk>/horarios/',        views_doctores.editar_horarios, name='horarios'),
]
