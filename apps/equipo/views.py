from .models import Equipo
from .models import Lugar
from .models import Componente
from .forms import EquipoForm
from django.utils import timezone
from apps.users.decorators import role_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from apps.users.models import UsersCustomUser

@role_required(roles=["admin", "tecnico"])
def equipo_view(request):
    # Solo los activos
    equipos = Equipo.objects.filter(fecha_eliminacion__isnull=True)
    return render(request, 'equipo/equipo_list.html', {'equipos': equipos})


@role_required(roles=["admin", "tecnico"])
def lista_equipos(request):
    try:
        equipos = Equipo.objects.select_related('id_lugar', 'id_users').all()
        componentes = Componente.objects.select_related('id_equipo').all()
        monitores = Componente.objects.filter(tipo__iexact="Monitor", fecha_eliminacion__isnull=True)
        impresoras = Componente.objects.filter(tipo__iexact="Impresora", fecha_eliminacion__isnull=True)

    except Exception as e:
        print("Error al consultar equipos:", e)
        equipos = []
        componentes = []
        monitores = []
        impresoras = []

    return render(request, 'equipo/partials/equipo_table.html', {
        'equipos': equipos,
        'componentes': componentes,
        'monitores': monitores,
        'impresoras': impresoras
    })



@role_required(roles=["admin", "tecnico"])
def editar_equipo(request, id):
    equipo = get_object_or_404(Equipo, id_equipo=id)
    usuarios = UsersCustomUser.objects.filter(is_active=True)  # Solo usuarios activos

    # Mostrar modal con datos
    if request.method == "GET" and request.headers.get("HX-Request"):
        form = EquipoForm(instance=equipo)
        return render(request, "equipo/partials/equipo_form.html", {
            "form": form,
            "equipo": equipo,
            "usuarios": usuarios,
        })

    # Guardar cambios
    if request.method == "POST":
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.modificado_por = request.user.username

            # 👇 Capturar el usuario seleccionado desde el dropdown
            user_id = request.POST.get("id_users")
            if user_id:
                equipo.id_users_id = user_id  # se asigna la FK directamente

            equipo.save()

            # Recargar tabla
            equipos = Equipo.objects.filter(fecha_eliminacion__isnull=True)
            if request.headers.get("HX-Request"):
                return render(request, "equipo/partials/equipo_table.html", {"equipos": equipos})

            return redirect("equipo:lista_equipos")

    return redirect("equipo:lista_equipos")
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   