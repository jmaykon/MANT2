from django.urls import path
from . import views

app_name = "mantenimiento"

urlpatterns = [
    path("lista/", views.mante_list, name="mante_list"),
    path("detalle/", views.mante_detalle, name="mante_detalle"),
    path("cronograma/", views.mante_cronograma, name="mante_cronograma"),
    path("solicitar/", views.mante_solicitar, name="mante_solicitar"),
    path("atender/", views.atender_ticket, name="atender_ticket"),
    path("get_ticket_data/<int:ticket_id>/", views.get_ticket_data, name="get_ticket_data"),
    
]
