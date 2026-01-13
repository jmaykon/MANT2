from django.urls import path
from . import views

app_name = 'lugar'

urlpatterns = [
    path('', views.lista_lugares, name='lista_lugares'),
    path('agregar/', views.agregar_lugares, name='agregar_lugares'),
    path('editar/<int:id>/', views.editar_lugar, name='editar_lugar'),
    path('eliminar/<int:id>/', views.eliminar_lugar, name='eliminar_lugar'),
]
