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
        ticket_id = request.POST.get('id_ticket')
        step = request.POST.get('step')

        ticket = get_object_or_404(Ticket, id_ticket=ticket_id)

        if step == '1':
            ticket.estado_ticket = 'pendiente'
            ticket.ultimo_paso = 1

        elif step == '2':
            ticket.estado_ticket = 'en_proceso'
            ticket.ultimo_paso = 2

        elif step == '3':
            ticket.estado_ticket = 'documentando'
            ticket.ultimo_paso = 3

            ticket.diagnostico = request.POST.get('diagnostico', '')
            ticket.solucion_aplicada = request.POST.get('solucion_aplicada', '')
            ticket.observaciones_tecnicas = request.POST.get('observaciones_tecnicas', '')
            ticket.comentario_usuario = request.POST.get('comentario_usuario', '')

        elif step == '4':
            ticket.estado_ticket = 'completado'
            ticket.ultimo_paso = 4
            ticket.fecha_cierre = timezone.now()

            ticket.diagnostico = request.POST.get('diagnostico', '')
            ticket.solucion_aplicada = request.POST.get('solucion_aplicada', '')
            ticket.observaciones_tecnicas = request.POST.get('observaciones_tecnicas', '')
            ticket.comentario_usuario = request.POST.get('comentario_usuario', '')            


        ticket.save()

        return JsonResponse({
            'estado': ticket.estado_ticket,
            'ultimo_paso': ticket.ultimo_paso
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from .models import Ticket  # Ajusta según tu modelo real

# apps/mantenimiento/views.py
from django.http import JsonResponse
from .models import Ticket

def get_ticket_data(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id_ticket=ticket_id)

        # Mapeo opcional: convertir estado_ticket a un "paso" numérico
        estado_a_paso = {
            'pendiente': 1,
            'en_proceso': 2,
            'documentando': 3,
            'completado': 4,
            'cancelado': 0,  # si quieres manejar cancelado como 0
        }
        paso_actual = estado_a_paso.get(ticket.estado_ticket, 1)

        data = {
            'id_ticket': ticket.id_ticket,
            'descripcion': ticket.descripcion or '',
            'diagnostico': ticket.diagnostico or '',
            'solucion': ticket.solucion_aplicada or '',
            'observaciones': ticket.observaciones_tecnicas or '',
            'comentario': ticket.comentario_usuario or '',
            'estado_ticket': ticket.estado_ticket,
            'paso_actual': paso_actual  # reemplaza 'ultimo_paso'
        }

        return JsonResponse(data)

    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


