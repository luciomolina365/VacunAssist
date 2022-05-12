from django.urls import path
from gestionVacunatorio.views import *


urlpatterns = [
    path('', home),
    path('foro', forum),
    path('inicioSesion', logIn, name="LogIn"),
    path('registrarse', signIn, name="SignIn"),
    path('saludo/', saludo),
]