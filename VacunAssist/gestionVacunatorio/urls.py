from django import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from gestionVacunatorio.views import *


app_name = 'main'
urlpatterns = [
    path('', home),

    

    path('saludo/', saludo, name='Saludo'),
    path("registro_de_usuario/", UserRegistration.as_view(), name="Registro"),
]

"""path('foro', forum),
    path('inicioSesion', logIn, name="LogIn"),
    path('registrarse', signIn, name="SignIn"),"""