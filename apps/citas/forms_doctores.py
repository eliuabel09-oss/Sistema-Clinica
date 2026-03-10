# apps/citas/forms_doctores.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model  = Doctor
        fields = [
            'nombres', 'apellidos', 'especialidad', 'cedula',
            'telefono', 'email', 'activo',
            'foto', 'biografia', 'horario_atencion',
        ]


class DoctorUsuarioForm(forms.Form):
    """Formulario para crear las credenciales de acceso del doctor."""
    username  = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'ej: dr.ramirez'})
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ese nombre de usuario ya está en uso.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned