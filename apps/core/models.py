# apps/core/models.py
from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('ADMIN',      'Administrador'),
        ('DOCTOR',     'Doctor'),
        ('SECRETARIA', 'Secretaria'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol     = models.CharField(max_length=20, choices=ROL_CHOICES, default='SECRETARIA')

    class Meta:
        db_table = 'perfiles_usuario'
        verbose_name = 'Perfil de Usuario'

    def __str__(self):
        return f'{self.usuario.username} — {self.get_rol_display()}'

    @property
    def es_admin(self):
        return self.rol == 'ADMIN' or self.usuario.is_superuser

    @property
    def es_doctor(self):
        return self.rol == 'DOCTOR'

    @property
    def es_secretaria(self):
        return self.rol == 'SECRETARIA'