# apps/consultas/admin.py
from django.contrib import admin
from .models import Consulta, Receta


class RecetaInline(admin.TabularInline):
    model         = Receta
    extra         = 1
    fields        = ['medicamento', 'dosis', 'frecuencia', 'duracion', 'indicaciones', 'orden']


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display  = ['paciente', 'doctor', 'fecha', 'diagnostico']
    search_fields = ['paciente__nombres', 'paciente__apellidos', 'diagnostico']
    list_filter   = ['doctor']
    ordering      = ['-fecha']
    list_per_page = 20
    inlines       = [RecetaInline]

    fieldsets = (
        ('Datos Generales', {
            'fields': ('cita', 'paciente', 'doctor')
        }),
        ('Signos Vitales', {
            'fields': (
                ('peso_kg', 'talla_cm'),
                ('presion_arterial', 'frecuencia_cardiaca'),
                ('temperatura', 'saturacion_o2'),
            ),
            'classes': ('collapse',)
        }),
        ('Nota Clinica SOAP', {
            'fields': ('subjetivo', 'objetivo', 'diagnostico', 'plan', 'evolucion')
        }),
        ('Seguimiento', {
            'fields': ('proxima_cita',)
        }),
    )


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display  = ['medicamento', 'dosis', 'frecuencia', 'duracion', 'consulta']
    search_fields = ['medicamento', 'consulta__paciente__nombres']
    list_per_page = 20
