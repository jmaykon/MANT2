from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_dashboard, name='admin'),  # fallback
    path('usuario/', views.home_dashboard, name='usuario'),
    path('tecnico/', views.home_dashboard, name='tecnico'),
    
]
