# apps/pacientes/urls.py
from django.urls import path
from . import views

app_name = 'pacientes'

urlpatterns = [
    path('',                   views.lista,         name='lista'),
    path('nuevo/',             views.crear,         name='crear'),
    path('<int:pk>/',          views.detalle,       name='detalle'),
    path('<int:pk>/editar/',   views.editar,        name='editar'),
    path('<int:pk>/eliminar/', views.eliminar,      name='eliminar'),
    path('<int:pk>/archivo/',  views.subir_archivo, name='subir_archivo'),
]