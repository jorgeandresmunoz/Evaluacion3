from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_salas, name='lista_salas'),
    path('sala/<int:sala_id>/', views.detalle_sala, name='detalle_sala'),
    path('reservar/<int:sala_id>/', views.reservar_sala, name='reservar_sala'),
    path('gestion/salas/', views.admin_salas, name='admin_salas'),
    path('gestion/salas/nueva/', views.crear_sala, name='crear_sala'),
    path('gestion/salas/<int:sala_id>/editar/', views.editar_sala, name='editar_sala'),
    path('gestion/salas/<int:sala_id>/eliminar/', views.eliminar_sala, name='eliminar_sala'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
]
