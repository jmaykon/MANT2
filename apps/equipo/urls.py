from django.urls import path
from . import views

app_name = 'equipo'

urlpatterns = [
    
    path('', views.equipo_view, name='equipo_view'),
    path('lista/', views.lista_equipos, name='lista_equipos'),
    path('editar/<int:id>/',views.editar_equipo, name ='editar_equipo'),
]

