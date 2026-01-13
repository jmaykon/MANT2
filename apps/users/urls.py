from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login_view, name='login'),              # Login raíz
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_users, name='perfil_users'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('users',views.user_list, name='user_list'),
    path('list/', views.user_list_view, name='user_list_view'),

]
