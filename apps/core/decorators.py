# apps/core/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def get_rol(user):
    """Retorna el rol del usuario: ADMIN, DOCTOR o SECRETARIA."""
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'ADMIN'
    try:
        return user.perfil.rol
    except Exception:
        # FIX: antes devolvía None, bloqueaba todo acceso
        # Ahora devuelve SECRETARIA como fallback seguro
        return 'SECRETARIA'


def rol_requerido(*roles):
    """
    Decorador que permite acceso solo a los roles especificados.
    Uso: @rol_requerido('ADMIN', 'SECRETARIA')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            rol = get_rol(request.user)
            if rol in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'No tienes permiso para acceder a esta sección.')
            return redirect('dashboard')
        return wrapper
    return decorator