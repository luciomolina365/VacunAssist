from django import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from gestionVacunatorio.views import *

app_name = 'main'
urlpatterns = [
    path('', home),

    

    path('saludo/', saludo, name='Saludo'),
    path("registro_de_usuario/", UserRegistration.as_view(), name="Registro"),
    path('inicio_de_sesion/', UserLogin.as_view(), name='Inicio_de_sesion')
    
]

"""path('foro', forum),
    path('inicioSesion', logIn, name="LogIn"),
    path('registrarse', signIn, name="SignIn"),"""