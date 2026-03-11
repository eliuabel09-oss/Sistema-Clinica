# apps/pacientes/forms.py
from django import forms
from .models import Paciente, ArchivoClinico


class PacienteForm(forms.ModelForm):
    class Meta:
        model  = Paciente
        fields = [
            'nombres', 'apellidos', 'fecha_nacimiento', 'sexo',
            'dni',                   # FIX: campo dni agregado
            'curp',                  # se mantiene opcional
            'tipo_sangre', 'telefono', 'email', 'direccion',
            'alergias', 'antecedentes', 'enfermedades_cronicas', 'activo',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class ArchivoClinicoForm(forms.ModelForm):
    class Meta:
        model  = ArchivoClinico
        fields = ['tipo', 'nombre', 'archivo', 'descripcion']