# apps/core/views_usuarios.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from apps.core.decorators import rol_requerido
from apps.core.models import PerfilUsuario


@login_required
@rol_requerido('ADMIN')
def lista(request):
    usuarios = User.objects.select_related('perfil').exclude(
        doctor_perfil__isnull=False  # excluir doctores (tienen su propio módulo)
    ).order_by('username')
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@login_required
@rol_requerido('ADMIN')
def crear(request):
    if request.method == 'POST':
        username   = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip()
        password1  = request.POST.get('password1', '')
        password2  = request.POST.get('password2', '')
        rol        = request.POST.get('rol', 'SECRETARIA')

        # Validaciones
        if not username:
            messages.error(request, 'El nombre de usuario es obligatorio.')
            return render(request, 'usuarios/form.html', {'post': request.POST})
        if User.objects.filter(username=username).exists():
            messages.error(request, f'El usuario "{username}" ya existe.')
            return render(request, 'usuarios/form.html', {'post': request.POST})
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'usuarios/form.html', {'post': request.POST})
        if len(password1) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return render(request, 'usuarios/form.html', {'post': request.POST})

        # Crear usuario
        user = User.objects.create_user(
            username   = username,
            password   = password1,
            first_name = first_name,
            last_name  = last_name,
            email      = email,
        )
        # Asignar rol
        perfil, _ = PerfilUsuario.objects.get_or_create(usuario=user)
        perfil.rol = rol
        perfil.save()

        messages.success(request, f'Usuario "{username}" creado correctamente.')
        return redirect('usuarios:lista')

    return render(request, 'usuarios/form.html')


@login_required
@rol_requerido('ADMIN')
def editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=usuario)

    # No permitir editar doctores desde aquí
    if hasattr(usuario, 'doctor_perfil'):
        messages.error(request, 'Los doctores se editan desde el módulo Doctores.')
        return redirect('usuarios:lista')

    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name', '').strip()
        usuario.last_name  = request.POST.get('last_name', '').strip()
        usuario.email      = request.POST.get('email', '').strip()
        perfil.rol         = request.POST.get('rol', 'SECRETARIA')

        # Cambiar contraseña solo si se llenó
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1:
            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'usuarios/form.html', {'usuario': usuario, 'perfil': perfil})
            if len(password1) < 6:
                messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
                return render(request, 'usuarios/form.html', {'usuario': usuario, 'perfil': perfil})
            usuario.set_password(password1)

        usuario.save()
        perfil.save()
        messages.success(request, f'Usuario "{usuario.username}" actualizado.')
        return redirect('usuarios:lista')

    return render(request, 'usuarios/form.html', {'usuario': usuario, 'perfil': perfil})


@login_required
@rol_requerido('ADMIN')
def eliminar(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    # No permitir eliminar al propio admin logueado
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('usuarios:lista')

    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado.')
    return redirect('usuarios:lista')