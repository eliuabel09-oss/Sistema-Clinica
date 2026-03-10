# apps/core/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import PerfilUsuario


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente un PerfilUsuario cada vez que se crea un User."""
    if created:
        rol = 'ADMIN' if instance.is_superuser else 'SECRETARIA'
        PerfilUsuario.objects.get_or_create(usuario=instance, defaults={'rol': rol})