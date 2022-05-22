from django import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from gestionVacunatorio.views import *

app_name = 'main'
urlpatterns = [
    path('', home),

    

    path('saludo/', saludo, name='Saludo'),
    path("registro_de_usuario/", UserRegistration.as_view(), name="Registro"),
    path('accounts/login/', UserLogin.as_view(), name='Inicio_de_sesion'),
    path('cambio_de_contraseña/', login_required(ChangeUserPassword.as_view()) , name="Cambiar_contraseña"),
    path('saludo/cierre_de_sesion/', logout_then_login, name = 'Cierre_de_sesion')
]
