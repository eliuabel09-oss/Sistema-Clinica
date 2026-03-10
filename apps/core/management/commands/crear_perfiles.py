# apps/core/management/__init__.py (vacío)
# apps/core/management/commands/__init__.py (vacío)

# apps/core/management/commands/crear_perfiles.py
#
# Ejecutar con: python manage.py crear_perfiles
#
# Crea el PerfilUsuario para los usuarios que ya existen en la BD
# sin borrar ni tocar nada más.
#
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.models import PerfilUsuario


class Command(BaseCommand):
    help = 'Crea PerfilUsuario para usuarios existentes que no lo tienen'

    def handle(self, *args, **kwargs):
        usuarios = User.objects.all()
        creados = 0
        for user in usuarios:
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={'rol': 'ADMIN' if user.is_superuser else 'SECRETARIA'}
            )
            if created:
                creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✅ Perfil creado: {user.username} → {perfil.get_rol_display()}')
                )
            else:
                self.stdout.write(f'  ℹ  Ya existe: {user.username} → {perfil.get_rol_display()}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Listo. {creados} perfiles nuevos creados.'))
        self.stdout.write('')
        self.stdout.write('Para asignar rol DOCTOR a un usuario de doctor:')
        self.stdout.write('  python manage.py shell')
        self.stdout.write('  >>> from apps.core.models import PerfilUsuario')
        self.stdout.write('  >>> p = PerfilUsuario.objects.get(usuario__username="nombre")')
        self.stdout.write('  >>> p.rol = "DOCTOR"')
        self.stdout.write('  >>> p.save()')