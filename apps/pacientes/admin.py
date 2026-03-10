# apps/pacientes/admin.py
from django.contrib import admin
from .models import Paciente, ArchivoClinico


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display  = ['apellidos', 'nombres', 'telefono', 'sexo', 'tipo_sangre', 'activo']
    search_fields = ['apellidos', 'nombres', 'curp', 'telefono']
    list_filter   = ['sexo', 'activo', 'tipo_sangre']
    ordering      = ['apellidos', 'nombres']
    list_per_page = 20

    fieldsets = (
        ('Datos Personales', {
            'fields': ('nombres', 'apellidos', 'fecha_nacimiento', 'sexo', 'curp', 'tipo_sangre')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion')
        }),
        ('Informacion Medica', {
            'fields': ('alergias', 'antecedentes', 'enfermedades_cronicas'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )


@admin.register(ArchivoClinico)
class ArchivoClinicoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'paciente', 'tipo', 'fecha_carga']
    search_fields = ['nombre', 'paciente__nombres', 'paciente__apellidos']
    list_filter   = ['tipo']
    ordering      = ['-fecha_carga']
    list_per_page = 20
