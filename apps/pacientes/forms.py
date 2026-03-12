# apps/pacientes/forms.py
import re
from django import forms
from .models import Paciente, ArchivoClinico


class PacienteForm(forms.ModelForm):
    class Meta:
        model  = Paciente
        fields = [
            'nombres', 'apellidos', 'fecha_nacimiento', 'sexo',
            'dni', 'curp', 'tipo_sangre', 'telefono', 'email', 'direccion',
            'alergias', 'antecedentes', 'enfermedades_cronicas', 'activo',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_nombres(self):
        v = self.cleaned_data.get('nombres', '').strip()
        if not v:
            raise forms.ValidationError('El nombre es obligatorio.')
        if len(v) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres.')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s\-]+$', v):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios.')
        return v.title()

    def clean_apellidos(self):
        v = self.cleaned_data.get('apellidos', '').strip()
        if not v:
            raise forms.ValidationError('Los apellidos son obligatorios.')
        if len(v) < 2:
            raise forms.ValidationError('Los apellidos deben tener al menos 2 caracteres.')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s\-]+$', v):
            raise forms.ValidationError('Los apellidos solo pueden contener letras y espacios.')
        return v.title()

    def clean_dni(self):
        v = self.cleaned_data.get('dni', '')
        if not v:
            return v
        v = v.strip()
        if not v.isdigit():
            raise forms.ValidationError('El DNI solo debe contener números.')
        if len(v) != 8:
            raise forms.ValidationError(f'El DNI debe tener exactamente 8 dígitos (ingresaste {len(v)}).')
        qs = Paciente.objects.filter(dni=v)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            otro = qs.first()
            raise forms.ValidationError(
                f'El DNI {v} ya está registrado para {otro.nombre_completo}.'
            )
        return v

    def clean_telefono(self):
        v = self.cleaned_data.get('telefono', '').strip()
        if not v:
            raise forms.ValidationError('El teléfono es obligatorio.')
        digitos = re.sub(r'[\s\-\+]', '', v)
        if not digitos.isdigit():
            raise forms.ValidationError('El teléfono solo debe contener números.')
        if len(digitos) == 9:
            if not digitos.startswith('9'):
                raise forms.ValidationError('Los celulares peruanos deben empezar con 9.')
        elif len(digitos) not in (7, 9):
            raise forms.ValidationError('El teléfono debe tener 7 dígitos (fijo) o 9 dígitos (celular).')
        return digitos

    def clean_email(self):
        v = self.cleaned_data.get('email', '')
        if not v:
            return v
        v = v.strip().lower()
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', v):
            raise forms.ValidationError('Ingresa un correo electrónico válido. Ej: nombre@correo.com')
        return v

    def clean_fecha_nacimiento(self):
        from datetime import date
        v = self.cleaned_data.get('fecha_nacimiento')
        if not v:
            raise forms.ValidationError('La fecha de nacimiento es obligatoria.')
        hoy = date.today()
        if v > hoy:
            raise forms.ValidationError('La fecha de nacimiento no puede ser en el futuro.')
        edad = (hoy - v).days // 365
        if edad > 120:
            raise forms.ValidationError('La fecha no parece válida (más de 120 años).')
        return v


class ArchivoClinicoForm(forms.ModelForm):
    class Meta:
        model  = ArchivoClinico
        fields = ['tipo', 'nombre', 'archivo', 'descripcion']

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede superar 10 MB.')
            ext = archivo.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']:
                raise forms.ValidationError(f'Formato .{ext} no permitido. Usa: PDF, JPG, PNG, DOC.')
        return archivo
