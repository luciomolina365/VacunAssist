from django import views
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from gestionVacunatorio.views import *

app_name = 'main'
urlpatterns = [
    
                       
    path('', home, name='homepage'),
    
    #path('cierre_de_sesion/', logout_then_login, name = 'Cierre_de_sesion')
    path('cierre_de_sesion/', logout_request, name = 'Cierre_de_sesion'),

##path user
    path('Home/', homeWithSession,name="homeS"),
    path("registro_de_usuario/", UserRegistration.as_view(), name="Registro"),
    path('accounts/login/', UserLogin.as_view(), name='Inicio_de_sesion'),
    path('formulario_de_ingreso/', login_required(FormularioDeIngreso.as_view()), name = 'Formulario_de_ingreso'),
    path("cambiar_nombre/",login_required (ChangeUserName.as_view()), name="Cambiar_nombre"),
    path("cambiar_email/",login_required (ChangeUserEmail.as_view()), name="Cambiar_email"),
    path('cambiar_datos/', ModificationManager, name='Modificacion_user'),
    path("cambio_de_zona/",login_required (ChangeUserZone.as_view()), name="Cambiar_zona"),
    path('cambio_de_contraseña/', login_required(ChangeUserPassword.as_view()) , name="Cambiar_contraseña"),
    path("turnos_pendientes/",ListUserTurn.as_view(), name = "Listar_Turnos"),
    path("historial_turnos/",ListUserHistory.as_view(), name = "Listar_Historial"),
    path("info_vacunatorios/",Info.as_view(), name = "Informacion"),
    path("solicitar_turno_fiebre_amarilla/",requestAmarillaTurn, name = "Solicitar_Amarilla"),
  



##path admin y vaccinator
    path('HomeAdmin/', homeAdmin ,name="homeA"),
    path('gestion_de_vacunadores/', vaccinatorManager, name='vaccinatorsM'),
    path('listar_historiales/', historyManager, name='historialVacunasM'),
    path("carga_usuario/", UserLoad.as_view(), name="Carga_de_usuario"),
    path("registrar_vacunador/",VaccinatorRegistration.as_view(), name="Registrar_Vacunador"),
    path("registrar_admin/",AdminRegistration.as_view(), name="Registrar_Admin"),
    path("listar_vacunadores/",ListVaccinator.as_view(), name = "Listar_Vacunadores"),
    path("foroAdmin/",ListForum.as_view(), name = "Foro_Admin"),
    path("listarTurnosDia/",ListTurnDay.as_view(), name = "Listar_Turnos_Dia"),
    path("modificar_post/<id>",modificar_foro, name ="Modificar_Post"),
    path("crear_post/",agregar_post, name ="Crear_Post"),

    path("listar_vacunatorios/",ListVaccination.as_view(), name = "Listar_Vacunatorios"),
    path("modificar_vacunatorio/<id>",modificar_vacunatorio, name ="Modificar_Vacunatorio"),
    
    path("listar_turno_zona/",ListTurnZone.as_view(), name = "Listar_Turnos_Zona"),
    path('accounts/admin_login/', staffLogin.as_view(), name='Inicio_de_sesion_staff'),
    path("listar_Covid/",ListCovid.as_view(), name = "Listar_Covid"),
    path("listar_Gripe/",ListGripe.as_view(), name = "Listar_Gripe"),
    path("listar_Amarilla/",ListAmarilla.as_view(), name = "Listar_Amarilla"),

    path("listar_solicitudes/",ListTurnRequests.as_view(), name = "Listar_solicitudes"),
    path("aceptar_solicitud/",SetTurnRequestDate.as_view(), name = "Aceptar_solicitud"),


    
    
]
