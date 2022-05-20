from django import views
from django.urls import path
from gestionVacunatorio.views import *


app_name = 'main'
urlpatterns = [
    path('', home),

    

    path('saludo/', saludo),
    path("registro_de_usuario/", userRegistration, name="Registro"),
    #path()
]

"""path('foro', forum),
    path('inicioSesion', logIn, name="LogIn"),
    path('registrarse', signIn, name="SignIn"),"""