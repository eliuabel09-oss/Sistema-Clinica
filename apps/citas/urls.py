# apps/citas/urls.py
from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('',                    views.lista,             name='lista'),
    path('nueva/',              views.crear,             name='crear'),
    path('<int:pk>/editar/',    views.editar,            name='editar'),
    path('<int:pk>/eliminar/',  views.eliminar,          name='eliminar'),
    path('<int:pk>/estado/',    views.cambiar_estado,    name='cambiar_estado'),

    # AJAX endpoints para el formulario inteligente
    path('ajax/doctores/',      views.ajax_doctores,     name='ajax_doctores'),
    path('ajax/horarios/',      views.ajax_horarios,     name='ajax_horarios'),
]
