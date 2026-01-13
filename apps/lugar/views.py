from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lugar
from .forms import LugarForm
from apps.users.decorators import role_required
from django.http import HttpResponse

@role_required(roles=["admin", "tecnico"])
def lista_lugares(request):
    lugares = Lugar.objects.filter(fecha_eliminacion__isnull=True)
    form = LugarForm()
    return render(request, 'lugar/lugar_list.html', {
        'lugares': lugares,
        'form': form
    })


@role_required(roles=["admin", "tecnico"])
def agregar_lugares(request):
    if request.method == "POST":
        form = LugarForm(request.POST)
        if form.is_valid():
            lugar = form.save(commit=False)
            lugar.creado_por = request.user.username
            lugar.save()

            response = render(
                request,
                "lugar/partials/lugar_table.html",
                {"lugares": Lugar.objects.filter(fecha_eliminacion__isnull=True)}
            )
            response["HX-Trigger"] = f'{{"lugarAgregado":"{lugar.nombre}"}}'
            return response
        
@role_required(roles=["admin", "tecnico"])
def editar_lugar(request, id):
    lugar = get_object_or_404(Lugar, id_lugar=id)

    if request.method == "GET" and request.headers.get("HX-Request"):
        form = LugarForm(instance=lugar)
        return render(request, "lugar/partials/lugar_edit_form.html", {"form": form, "lugar": lugar})

    if request.method == "POST" and request.headers.get("HX-Request"):
        form = LugarForm(request.POST, instance=lugar)
        if form.is_valid():
            lugar = form.save(commit=False)
            lugar.modificado_por = request.user.username
            lugar.save()

            response = render(
                request,
                "lugar/partials/lugar_table.html",
                {"lugares": Lugar.objects.filter(fecha_eliminacion__isnull=True)}
            )
            response["HX-Trigger"] = f'{{"lugarEditado":"{lugar.nombre}"}}'
            return response

@role_required(roles=["admin", "tecnico"])
def eliminar_lugar(request, id):
    if request.headers.get("HX-Request"):
        lugar = get_object_or_404(Lugar, id_lugar=id)
        nombre = lugar.nombre

        lugar.fecha_eliminacion = timezone.now()
        lugar.eliminado_por = request.user.username
        lugar.save()

        response = render(
            request,
            "lugar/partials/lugar_table.html",
            {"lugares": Lugar.objects.filter(fecha_eliminacion__isnull=True)}
        )
        response["HX-Trigger"] = f'{{"lugarEliminado":"{nombre}"}}'
        return response
