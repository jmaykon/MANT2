from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json

# Importaciones de tu proyecto
from apps.users.decorators import role_required 
from .models import Ticket, Notificacion, HistorialTicket

@login_required
@role_required(roles=["admin", "tecnico","usuario"])
def mante_list(request):
    tickets = Ticket.objects.all().order_by('-fecha_creacion')
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
        tipo = request.POST.get('tipo')
        colores = request.POST.getlist('colores')
        descripcion = request.POST.get('descripcion')
        prioridad = request.POST.get('prioridad', 'media')

        if tipo == 'recarga_tinta' and not colores:
            return HttpResponse("Por favor, seleccione al menos un color.", status=400)

        try:
            if tipo == 'recarga_tinta':
                detalle = "Todos los colores" if "todos" in colores else ", ".join(colores).title()
            elif tipo == 'tonner':
                detalle = "Recarga de Tonner"
            elif tipo == 'soporte_usuario':
                detalle = "Soporte Técnico Directo"
            else:
                detalle = "Mantenimiento General"

            nuevo_ticket = Ticket.objects.create(
                id_users=request.user,
                tipo_soporte=tipo,
                insumos_utilizados=detalle,
                descripcion=descripcion,
                estado_ticket='Pendiente',
                prioridad=prioridad,
                creado_por=request.user.username
            )

            response = HttpResponse("") 
            response['HX-Trigger'] = json.dumps({
                "eventoTicketCreado": {"numero": nuevo_ticket.id_ticket}
            })
            return response

        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return render(request, 'mantenimiento/mante_solicitar.html')

# --- ESTA ES LA FUNCIÓN QUE CAUSABA EL ERROR ---
@login_required
def atender_ticket(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(Ticket, id_ticket=ticket_id)
        
        ticket.diagnostico = request.POST.get('diagnostico')
        ticket.solucion_aplicada = request.POST.get('solucion_aplicada')
        ticket.observaciones_tecnicas = request.POST.get('observaciones_tecnicas')
        ticket.comentario_usuario = request.POST.get('comentario_usuario')
        
        ticket.estado_ticket = 'completado'
        ticket.fecha_cierre = timezone.now()
        ticket.save()
        
        messages.success(request, f"¡Ticket #{ticket_id} finalizado con éxito!")
        
    # El nombre de la URL de tu lista es 'mante_list' según tus logs
    return redirect('mantenimiento:mante_list')