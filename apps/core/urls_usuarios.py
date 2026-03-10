# apps/core/urls_usuarios.py
from django.urls import path
from . import views_usuarios

app_name = 'usuarios'

urlpatterns = [
    path('',                   views_usuarios.lista,    name='lista'),
    path('nuevo/',             views_usuarios.crear,    name='crear'),
    path('<int:pk>/editar/',   views_usuarios.editar,   name='editar'),
    path('<int:pk>/eliminar/', views_usuarios.eliminar, name='eliminar'),
]