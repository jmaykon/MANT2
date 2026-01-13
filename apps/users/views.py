from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import LoginForm
from .models import UsersCustomUser
from apps.users.decorators import role_required
from .models import Equipo
from .models import Lugar
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .forms import UserCreateForm  # Importa el formulario que creamos



# -------------------- LOGIN --------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirigir según rol
            if user.role == 'admin':
                return redirect('dashboard:admin')
            elif user.role == 'tecnico':
                return redirect('dashboard:tecnico')
            elif user.role == 'usuario':
                return redirect('dashboard:usuario')
    else:
        form = LoginForm()
    return render(request, 'users/user_login.html', {'form': form})

# -------------------- PERFIL --------------------
@role_required(roles=["admin","tecnico","usuario"])
def perfil_users(request):
    return render(request, 'users/user_perfil.html')

# -------------------- EDITAR PERFIL --------------------
@role_required(roles=["admin","tecnico","usuario"])
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, '✅ Perfil actualizado correctamente.')
        return redirect('users:perfil_users')
    else:
        return render(request, 'users/user_editar_perfil.html')

# -------------------- CAMBIAR CONTRASEÑA --------------------
@role_required(roles=["admin","tecnico"])
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '🔒 Contraseña actualizada correctamente.')
            return redirect('users:perfil_users')
        else:
            messages.error(request, '⚠ Error al cambiar la contraseña. Verifique los campos.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/user_cambiar_password.html', {'form': form})

# -------------------- LOGOUT --------------------
@role_required(roles=["admin","tecnico","usuario"])
def logout_view(request):
    logout(request)
    messages.info(request, '👋 Sesión cerrada correctamente.')
    return redirect('users:login')



@role_required(roles=["admin","tecnico"])
def user_list(request):

    try:
        
        
        users = UsersCustomUser.objects.select_related('id_lugar', 'id_equipo').all()
        equipo = Equipo.objects.all()
        lugar = Lugar.objects.all()
        users = UsersCustomUser.objects.all()
    except Exception as e:
        print("Error al consultar usuarios:", e)
    return render(request, 'users/user_list.html', {'users': users, 'equipos': equipo, 'lugares': lugar})

@role_required(roles=["admin","tecnico"])
def usuarios_dashboard(request):
    users = UsersCustomUser.objects.all()
    equipos = Equipo.objects.all()
    lugares = Lugar.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(UsersCustomUser, id=user_id)
        form = UsersCustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard:usuarios')  # Ajusta tu namespace/url

    return render(request, 'dashboard/usuarios.html', {
        'users': users,
        'equipos': equipos,
        'lugares': lugares,
    })
    
    

@role_required(roles=["admin","tecnico"])
@csrf_exempt
def guardar_usuario(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        role = request.POST.get('role')
        id_equipo = request.POST.get('id_equipo') or None
        id_lugar = request.POST.get('id_lugar') or None
        is_active = True if request.POST.get('is_active') == 'on' else False
        firma = request.FILES.get('firma')

        # Campos opcionales
        nombre = request.POST.get('nombre') or None
        apellido_p = request.POST.get('apellido_p') or None
        apellido_m = request.POST.get('apellido_m') or None
        telefono = request.POST.get('telefono') or None
        email = request.POST.get('email') or None

        # Password: primeras 3 letras del rol + código
        raw_password = (role[:3] + codigo).lower()
        password = make_password(raw_password)

        username = role.lower()
        is_superuser = True if role.lower() == 'admin' else False
        is_staff = 1 if is_active else 0

        user = UsersCustomUser.objects.create(
            username=username,
            password=password,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
            date_joined=timezone.now(),
            role=role.lower(),
            firma=firma,
            nombre=nombre,
            apellido_p=apellido_p,
            apellido_m=apellido_m,
            telefono=telefono,
            email=email,
            id_lugar_id=id_lugar,
            id_equipo_id=id_equipo,
            codigo=codigo
        )

        return redirect('users:user_list') 

    return redirect('users:user_list')


@login_required # Asegúrate de proteger esta vista
def user_list_view(request):
    
    if request.method == 'POST':
        # 1. Si es POST, creamos el usuario
        # Pasamos request.POST (datos) y request.FILES (para la 'firma')
        form = UserCreateForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado con éxito.')
            # Redirigimos a la misma vista con GET para limpiar el form
            return redirect('users:user_list') 
        else:
            # 2. Si el formulario es inválido, los errores se mostrarán en el modal
            messages.error(request, 'Error al crear el usuario. Revisa los campos.')
            # No redirigimos, dejamos que la vista continúe para renderizar
            # la página con el 'form' que contiene los errores.
    
    else:
        # 3. Si es GET, creamos un formulario vacío
        form = UserCreateForm()

    # 4. En cualquier caso (GET o POST fallido), preparamos el contexto
    users = User.objects.all().order_by('id')
    # No necesitas 'equipos' y 'lugares' aquí, el 'form' ya los maneja
    # (aunque tu plantilla los usa en el modal, así que los dejamos)
    equipos = Equipo.objects.all()
    lugares = Lugar.objects.all()

    context = {
        'users': users,
        'equipos': equipos, # Necesario para el <select> manual (si se mantiene)
        'lugares': lugares, # Necesario para el <select> manual (si se mantiene)
        'form': form,       # ¡El contexto más importante!
    }
    
    return render(request, 'users/user_list.html', context)



