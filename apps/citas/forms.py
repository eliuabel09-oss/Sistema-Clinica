# apps/citas/forms.py
from django import forms
from .models import Cita


class CitaForm(forms.ModelForm):
    class Meta:
        model  = Cita
        fields = ['paciente', 'doctor', 'fecha_hora', 'duracion_min', 'tipo', 'estado', 'motivo', 'notas_admin']
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aceptar ambos formatos que puede enviar el formulario inteligente
        self.fields['fecha_hora'].input_formats = [
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%d/%m/%Y %H:%M',
        ]
        if self.instance and self.instance.fecha_hora:
            self.initial['fecha_hora'] = self.instance.fecha_hora.strftime('%Y-%m-%dT%H:%M')
