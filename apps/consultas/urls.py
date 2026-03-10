# apps/consultas/urls.py
from django.urls import path
from . import views

app_name = 'consultas'

urlpatterns = [
    path('',          views.lista,   name='lista'),
    path('nueva/',    views.crear,   name='crear'),
    path('<int:pk>/', views.detalle, name='detalle'),
]