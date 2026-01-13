# apps/mantenimiento/views.py

from django.shortcuts import render, redirect
from apps.users.decorators import role_required 
from apps.mantenimiento.models import Ticket
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Notificacion
from django.http import HttpResponse  
import json
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Ticket
from apps.mantenimiento.models import Ticket
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Ticket, HistorialTicket
from django.contrib.auth.decorators import login_required
@login_required
@role_required(roles=["admin", "tecnico","usuario"])
def mante_list(request):
    tickets = Ticket.objects.all().order_by('-fecha_creacion')  # Ordenados por fecha reciente
    return render(request, "mantenimiento/mante_list.html", {'tickets': tickets})



@role_required(roles=["admin", "tecnico","usuario"])
def mante_detalle(request):
    return render(request, "mantenimiento/mante_detalle.html")

@role_required(roles=["admin","usuario"])
def mante_cronograma(request):
    return render(request, "mantenimiento/mante_cronograma.html")


@login_required
@role_required(roles=["admin", "usuario"])
def mante_solicitar(request):
    if request.method == 'POST':
        # 1. Captura de datos del formulario
        tipo = request.POST.get('tipo')
        colores = request.POST.getlist('colores')
        descripcion = request.POST.get('descripcion')
        prioridad = request.POST.get('prioridad', 'media')  # valor por defecto 'media'

        # 2. Validación de negocio: Tinta obligatoria
        if tipo == 'recarga_tinta' and not colores:
            return HttpResponse("Por favor, seleccione al menos un color para la recarga.", status=400)

        try:
            # 3. Procesamiento del detalle de insumos según el tipo
            if tipo == 'recarga_tinta':
                detalle = "Todos los colores" if "todos" in colores else ", ".join(colores).title()
            elif tipo == 'tonner':
                detalle = "Recarga de Tonner"
            elif tipo == 'soporte_usuario':
                detalle = "Soporte Técnico Directo"
            else:
                detalle = "Mantenimiento General"

            # 4. Creación del registro en la base de datos con prioridad
            nuevo_ticket = Ticket.objects.create(
                id_users=request.user,
                tipo_soporte=tipo,
                insumos_utilizados=detalle,
                descripcion=descripcion,
                estado_ticket='Pendiente',
                prioridad=prioridad,  # <--- Aquí se guarda la prioridad
                creado_por=request.user.username  # Auditoría
            )

            # 5. Respuesta exitosa con el disparador (Trigger) para SweetAlert
            response = HttpResponse("") 
            response['HX-Trigger'] = json.dumps({
                "eventoTicketCreado": {
                    "numero": nuevo_ticket.id_ticket
                }
            })
            return response

        except Exception as e:
            print(f"Error al crear ticket: {e}")
            return HttpResponse("Error interno al procesar la solicitud.", status=500)

    # Si la petición es GET, renderizamos el formulario inicial
    return render(request, 'mantenimiento/mante_solicitar.html')


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.mantenimiento.models import Ticket, HistorialTicket
from django.utils import timezone

@login_required
def atender_ticket(request):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id_ticket=request.POST.get("ticket_id"))

        # Actualizamos estado
        nuevo_estado = request.POST.get("estado_ticket")
        if nuevo_estado and ticket.estado_ticket != nuevo_estado:
            HistorialTicket.objects.create(
                ticket=ticket,
                estado_anterior=ticket.estado_ticket,
                estado_nuevo=nuevo_estado,
                usuario=request.user
            )
            ticket.estado_ticket = nuevo_estado.lower()

        # Actualizamos campos técnicos
        ticket.diagnostico = request.POST.get("diagnostico", ticket.diagnostico)
        ticket.solucion_aplicada = request.POST.get("solucion_aplicada", ticket.solucion_aplicada)
        ticket.observaciones_tecnicas = request.POST.get("observaciones_tecnicas", ticket.observaciones_tecnicas)
        ticket.comentario_usuario = request.POST.get("comentario_usuario", ticket.comentario_usuario)

        if nuevo_estado == "en_proceso" and not ticket.fecha_inicio:
            ticket.fecha_inicio = timezone.now()
        if nuevo_estado == "completado" and not ticket.fecha_cierre:
            ticket.fecha_cierre = timezone.now()

        ticket.modificado_por = request.user
        ticket.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Método no permitido"}, status=405)


























