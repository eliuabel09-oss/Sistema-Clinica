# apps/consultas/urls.py
from django.urls import path
from . import views, views_pdf

app_name = 'consultas'

urlpatterns = [
    path('',               views.lista,    name='lista'),
    path('nueva/',         views.crear,    name='crear'),
    path('<int:pk>/',      views.detalle,  name='detalle'),
    path('<int:pk>/eliminar/', views.eliminar, name='eliminar'),  # FIX: faltaba esta URL
    path('<int:pk>/receta-pdf/', views_pdf.receta_pdf, name='receta_pdf'),
]