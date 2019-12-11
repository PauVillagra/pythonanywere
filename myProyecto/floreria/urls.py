from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('home_administrador/',home_administrador,name='home_administrador'),
    path('home_usuario/',home_usuario,name='home_usuario'),
    path('galeria_administrador/',galeria_administrador,name='galeria_administrador'),
    path('galeria_usuario/',galeria_usuario,name='galeria_usuario'),
    path('formulario/',formulario,name='formulario'),
    path('eliminar_flor/<id>/',eliminar_flor,name='eliminar'),
    path('',login,name='login'),
    path('login_inicio/',login_inicio,name='login_inicio'),
    path('cerrar_sesion/',cerrar_sesion,name='cerrar_sesion'),
    path('carrito/',carrito,name='CARRITO'),
    path('carro_mas/<id>/',carro_compras_mas,name='CARRO_MAS'),
    path('carro_menos/<id>/',carro_compras_menos,name='CARRO_MENOS'),
    path('grabar_carro/',grabar_carro,name='GRABAR_CARRO'),
    path('agregar_carro/<id>/',agregar_carro,name='AGREGAR_CARRO'), 
    path('vaciar_carrito/',vaciar_carrito,name='VACIAR'),
    path('registro/',registro,name='registro'),
]