# apps/citas/forms_doctores.py
import re
from django import forms
from django.contrib.auth.models import User
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model  = Doctor
        fields = [
            'nombres', 'apellidos', 'especialidad', 'cedula',
            'telefono', 'email', 'activo', 'foto', 'biografia', 'horario_atencion',
        ]

    def clean_nombres(self):
        v = self.cleaned_data.get('nombres', '').strip()
        if not v:
            raise forms.ValidationError('El nombre es obligatorio.')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s\-]+$', v):
            raise forms.ValidationError('El nombre solo debe contener letras.')
        return v.title()

    def clean_apellidos(self):
        v = self.cleaned_data.get('apellidos', '').strip()
        if not v:
            raise forms.ValidationError('Los apellidos son obligatorios.')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s\-]+$', v):
            raise forms.ValidationError('Los apellidos solo deben contener letras.')
        return v.title()

    def clean_cedula(self):
        v = self.cleaned_data.get('cedula', '').strip()
        if not v:
            raise forms.ValidationError('El número de cédula/colegiatura es obligatorio.')
        qs = Doctor.objects.filter(cedula=v)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(f'Ya existe un doctor registrado con la cédula "{v}".')
        return v

    def clean_telefono(self):
        v = self.cleaned_data.get('telefono', '').strip()
        if not v:
            return v
        digitos = re.sub(r'[\s\-\+]', '', v)
        if not digitos.isdigit():
            raise forms.ValidationError('El teléfono solo debe contener números.')
        if len(digitos) == 9 and not digitos.startswith('9'):
            raise forms.ValidationError('Los celulares peruanos deben empezar con 9.')
        if len(digitos) not in (7, 9):
            raise forms.ValidationError('El teléfono debe tener 7 dígitos (fijo) o 9 dígitos (celular).')
        return digitos

    def clean_email(self):
        v = self.cleaned_data.get('email', '').strip().lower()
        if not v:
            return v
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', v):
            raise forms.ValidationError('Ingresa un correo electrónico válido.')
        return v

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto and hasattr(foto, 'size'):
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La foto no puede superar 5 MB.')
            ext = foto.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise forms.ValidationError('Solo se permiten imágenes JPG, PNG o WEBP.')
        return foto


class DoctorUsuarioForm(forms.Form):
    username  = forms.CharField(label='Nombre de usuario', max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'ej: dr.ramirez'}))
    password1 = forms.CharField(label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    password2 = forms.CharField(label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

    def clean_username(self):
        v = self.cleaned_data.get('username', '').strip().lower()
        if not v:
            raise forms.ValidationError('El nombre de usuario es obligatorio.')
        if not re.match(r'^[a-z0-9_.\-]+$', v):
            raise forms.ValidationError('Solo letras minúsculas, números, puntos y guiones.')
        if User.objects.filter(username=v).exists():
            raise forms.ValidationError(f'El usuario "{v}" ya está en uso. Prueba con otro.')
        return v

    def clean_password1(self):
        p = self.cleaned_data.get('password1', '')
        if len(p) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        return p

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned
