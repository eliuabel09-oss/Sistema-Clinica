# apps/citas/admin.py
from django.contrib import admin
from .models import Doctor, Cita


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display  = ['apellidos', 'nombres', 'especialidad', 'cedula', 'telefono', 'activo']
    search_fields = ['apellidos', 'nombres', 'cedula', 'especialidad']
    list_filter   = ['especialidad', 'activo']
    ordering      = ['apellidos', 'nombres']
    list_per_page = 20


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display  = ['paciente', 'doctor', 'fecha_hora', 'tipo', 'estado', 'duracion_min']
    search_fields = ['paciente__nombres', 'paciente__apellidos', 'doctor__apellidos']
    list_filter   = ['estado', 'tipo', 'doctor']
    ordering      = ['-fecha_hora']
    list_per_page = 20
    date_hierarchy = 'fecha_hora'

    fieldsets = (
        ('Informacion de la Cita', {
            'fields': ('paciente', 'doctor', 'fecha_hora', 'duracion_min', 'tipo')
        }),
        ('Estado', {
            'fields': ('estado', 'motivo', 'notas_admin')
        }),
    )
