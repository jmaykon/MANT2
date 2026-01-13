from django.urls import path
from . import views

app_name = "mantenimiento"  # 👈 namespace correcto

urlpatterns = [
    
    path("lista/", views.mante_list, name="mante_list"),
    path("detalle", views.mante_detalle, name="mante_detalle"),
    path("cronograma/", views.mante_cronograma, name="mante_cronograma"),
    path("solicitar/", views.mante_solicitar, name="mante_solicitar"),

]
