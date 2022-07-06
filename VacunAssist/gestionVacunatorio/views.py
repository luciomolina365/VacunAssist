from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template import Context, Template
from .models import UserManager
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import Vaccinator, User, Turn, Formulary,Information
from .mail.send_email import *
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.urls import reverse

def saludo(request):
    return render(request, 'prueba.html')

def home(request):
    return render(request,'indexHome.html')

def homeAdmin(request):
    return render(request,'homeAdmin.html')

def homeWithSession(request):
    #print(request.user.id)
    user = User.objects.filter(id = request.user.id)
    user = user.first()
    if user != None:
        #print("Usuario existe")
        formulary1 = Formulary.objects.filter(user_id = request.user.id)
        formulary1 = formulary1.first()
        if formulary1 != None:
            #print(formulary1)
            #print('Tengo formulario')
            return render(request,'homeWithSession.html')
        else:
            #print("NO tengo formulario") 
            return redirect(reverse_lazy('main:Formulario_de_ingreso'))
            

    return render(request,'homeWithSession.html') #POR LAS DUDAS

def requestAmarillaTurn(request):

    def requestTurn(request, user, date = None):
        vacuna = Vaccine.objects.filter(name="AMARILLA").first()
        #SI NO HAY VACUNA 
        if vacuna == None:
            vacuna = Vaccine.objects.create(name="AMARILLA", timeSpan=1)
            vacuna = Vaccine.objects.filter(name="AMARILLA").first()
        
        formulario1 = Formulary.objects.filter(user = user).first()
        #SI TIENE FORMULARIO
        if formulario1 != None:
            #SI TIENE LA VACUNA
            if formulario1.amarilla_ok == True:
                messages.error(request, "Usted ya tiene la vacuna de la fiebre amarilla.")
                return render(request,'homeWithSession.html')

            #SI ///NO/// TIENE LA VACUNA |||Y||| YA TIENE UNA SOLICITUD PENDIENTE
            aux_turn = Turn.objects.filter(user = user) 
            aux_turn = aux_turn.filter(date = None).first()
            #print(aux_turn)
            if formulario1.amarilla_ok == False and aux_turn != None:
                messages.error(request, "Usted ya tiene una solicitud pendiente.")
                return render(request,'homeWithSession.html')

            #SI ///NO/// TIENE LA VACUNA
            if formulario1.amarilla_ok == False:
                date = datetime.today().__add__(timedelta(days=365)) # DENTRO DE UN AÑO
                Turn.objects.create(user = user, vaccine = vacuna, status = False, date = None, accepted = False)
                messages.success(request, "Solicitud exitosa.")
                return render(request,'homeWithSession.html')
        else:
            messages.error(request, "Usted no completó el formulario de ingreso.")
            return render(request,'homeWithSession.html') 

    user = User.objects.filter(id = request.user.id)
    user = user.first()
    if user != None:
        formulary1 = Formulary.objects.filter(user_id = request.user.id)
        formulary1 = formulary1.first()
        if formulary1 != None:
            requestTurn(request, user, date = None)
            return render(request,'homeWithSession.html')
        else:
            #mensaje de error??
            return redirect(reverse_lazy('main:Formulario_de_ingreso'))
            

    return render(request,'homeWithSession.html') #POR LAS DUDAS
    
    

def ModificationManager(request):
    return render(request,'modificationManager.html')

def vaccinatorManager(request):
    return render(request,'vaccinatorsManager.html')

class UserRegistration(CreateView):
    model = User
    form_class = UserRegForm
    template_name = 'registration/signIn.html'
    success_url = reverse_lazy('main:Inicio_de_sesion')

    def form_valid(self, form):
        messages.success(self.request,"Registro exitoso")
        print(form)
        return super(UserRegistration, self).form_valid(form)
    
class VaccinatorRegistration(CreateView):
    model = Vaccinator
    form_class = VaccinatorRegForm
    template_name = 'registration/registerVaccinator.html'
    success_url = reverse_lazy('main:homeA')

    def form_valid(self, form):
        messages.success(self.request,"Registro exitoso")
        return super(VaccinatorRegistration, self).form_valid(form)

class AdminRegistration(CreateView):
    model = Admin
    form_class = AdminRegForm
    template_name = 'registration/registerAdmin.html'
    success_url = reverse_lazy('main:Inicio_de_sesion_staff')   

def logout_request(request):
    logout(request)
    messages.info(request, "Cierre de sesión exitoso")
    return redirect('main:homepage')

class UserLogin(FormView):
    template_name = "login/user_login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy('main:homeS')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(UserLogin,self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        dato=Formulary.objects.filter(user=self.request.user)
        #print(dato.first())
        messages.success(self.request,"Inicio de sesion exitoso")
        if (dato.first()== None):
            new_url = reverse_lazy('main:Formulario_de_ingreso')
            return HttpResponseRedirect(new_url)
            
        return super(UserLogin, self).form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

def custom_logout(request):
    #print('Loggin out {}'.format(request.user))
    logout(request)
    #print(request.user)
    return render(request,'indexHome.html')

class ChangeUserPassword(View):
    template_name = "modification/changePass.html"
    form_class = ChangeUserPasswordForm
    success_url = reverse_lazy('main:Inicio_de_sesion') #cambiar

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(id = request.user.id)
            if user.exists():
                user = user.first()
                user.set_password(form.cleaned_data.get('password1'))
                send_passwordConfirm_email(user.email,user.name)
                user.save()
                messages.success(request,"Cambio de Contraseña exitoso")
                return redirect(self.success_url)

            return redirect(self.success_url)
            
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form':form})
            
class ChangeUserName(View):
    template_name = "modification/changeName.html"
    form_class = ChangeUserNameForm
    success_url = reverse_lazy('main:homeS') #CAMBIAR

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(id = request.user.id)
            if user.exists():
                user = user.first()
                user.set_new_name(form.cleaned_data.get('name'))
                user.save()
                messages.success(request,"Cambio de nombre exitoso")
                return redirect(self.success_url)

            return redirect(self.success_url)
            
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form':form})

class UserLoad(CreateView):
    model = User
    form_class = UserRegForm
    template_name = 'registration/addUser.html'
    success_url = reverse_lazy('main:homeA')

class ChangeUserEmail(View):
    template_name = "modification/changeUserEmail.html"
    form_class = ChangeUserEmailForm
    success_url = reverse_lazy('main:homeS') #CAMBIAR

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(id = request.user.id)
            if user != None:
                user = user.first()
                exist=User.objects.filter(email = request.POST["email1"])
                #print(exist.first())
                if exist.first() == None:
                    user.set_new_email(form.cleaned_data.get('email1'))
                    user.save()
                    return redirect(self.success_url)
                else:
                    messages.error(request,"Ya existe un usuario con ese e-mail. Por favor ingrese uno diferente. ")

            return render(request, self.template_name, {'form':form })
            
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form':form })


class ChangeUserZone(View):
    template_name = "modification/changeUserZone.html"
    form_class = ChangeUserZoneForm
    success_url = reverse_lazy('main:homeS')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(id = request.user.id)
            if user != None:
                user = user.first()
                user.set_new_zone(form.cleaned_data.get('zone'))
                user.save()
                messages.success(request,"La modificacion de su nueva zona a sido un exito ")
                return redirect(self.success_url)
            
            return render(request, self.template_name, {'form':form })
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form':form })



class ListUserTurn(View):
    template_name = "listUserTurn.html"

    def get(self, request, *args, **kwargs):   
        try:
            turnos=Turn.objects.order_by("date").filter(user_id=request.user.id)
            turns=[] 
            for t in turnos:
                if (t.date >= date.today()):
                    aux=t
                    aux.vaccine_id=Vaccine.objects.get(id = t.vaccine_id)
                    aux.user_id=request.user.name
                    aux.zone=request.user.zone
                    turns.append(aux)
                else:
                    pass
        except Turn.DoesNotExist:
            pass
        if len(turns) == 0:
            messages.success(request, "Usted no posee turnos pendientes")

        return render(request, self.template_name, {'turnos': turns})

class ListUserHistory(View):
    template_name = "listUserHistory.html"

    def get(self, request, *args, **kwargs):   
        try:
            turnos=Turn.objects.order_by("date").filter(user_id=request.user.id)
            turns=[] 
            for t in turnos:
                if t.date != None:
                    if (t.date < date.today() and t.status== True):
                        aux=t
                        aux.vaccine_id=Vaccine.objects.get(id = t.vaccine_id)
                        aux.user_id=request.user.name
                        aux.zone=request.user.zone
                        turns.append(aux)
                    else:
                        pass
        except Turn.DoesNotExist:
            pass
        if len(turns) == 0:
            messages.success(request, "Usted no posee turnos en su historial")

        return render(request, self.template_name, {'turnos': turns})


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Staff

class staffLogin(FormView):
    template_name = "login/staff_login.html"
    form_class = VaccinatorLoginForm
    success_url = reverse_lazy('main:homeA')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args,**kwargs):
        if len(request.POST) != 0:
            try:
                try:
                    if (request.POST['username']== "admin"):
                        m= Admin.objects.get(name=request.POST['username'])
                        zona = None
                    else:
                        m = Vaccinator.objects.get(email=request.POST['username'])
                        zona= m.zone
                except Admin.DoesNotExist:
                    raise Vaccinator.DoesNotExist
                if m.check_password(request.POST['password']):
                    request.session['user'] = {"name":m.name,"admin":m.is_admin,"zone":zona}
                    messages.success(request,"Inicio de sesion exitoso. ")
                    return HttpResponseRedirect(self.get_success_url())
            except Vaccinator.DoesNotExist:
                pass
        return super(staffLogin,self).dispatch(request,*args, **kwargs)

class ListVaccinator(View):
    template_name = "listVaccinators.html"

    def get(self, request, *args, **kwargs):
        vaccinators = Vaccinator.objects.all()
        return render(request, self.template_name, {'vacunadores': vaccinators})

    def post(self, request, *args, **kwargs):
        vaccinator = Vaccinator.objects.get(id=request.POST["vacunador_id"])
        vaccinator.delete()
        messages.success(request," Eliminacion exitosa. ")
        vaccinators = Vaccinator.objects.all()
        return render(request, self.template_name, {'vacunadores': vaccinators})

        
class ListUsers(View):
    template_name = "listUsers.html"

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, self.template_name, {'usuarios': users})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.POST["usuario_id"])
        user.delete()
        messages.success(request," Eliminacion exitosa. ")
        users = User.objects.all()
        return render(request, self.template_name, {'usuarios': users})

class ListTurnZone(View):
    template_name = "listTurnZone.html"

    def get(self, request, *args, **kwargs):
        zoneFilter=request.session['user']['zone']
        data=[]
        users=User.objects.filter(zone=zoneFilter)
        for u in users:
            try:
                aux=Turn.objects.order_by("date").filter(user_id = u.id)
                for t in aux:
                    if t.date != None:
                        if ((t.date >= date.today()) and (t.status == False)):
                            turn=t
                            turn.vaccine_id=Vaccine.objects.get(id = t.vaccine_id)
                            turn.user_id=User.objects.get(id = t.user_id)
                            data.append(turn)
            except Turn.DoesNotExist:
                pass
        if len(data) == 0:
            messages.success(request, "No hay turnos en la zona")

        return render(request, self.template_name, {'turnos': data})


    def post(self, request, *args, **kwargs):
        turn = Turn.objects.get(id=request.POST["turno_id"])
        turn.status=True
        turn.save()
        messages.success(request,"Ha marcado como presente el turno seleccionado")
        zoneFilter=request.session['user']['zone']
        data=[]
        users=User.objects.filter(zone=zoneFilter)
        for u in users:
            try:
                aux=Turn.objects.order_by("date").filter(user_id = u.id)
                for t in aux:
                    if t.date != None:
                        if ((t.date >= date.today()) and (t.status == False)):
                            turn=t
                            turn.vaccine_id=Vaccine.objects.get(id = t.vaccine_id)
                            turn.user_id=User.objects.get(id = t.user_id)
                            data.append(turn)
            except Turn.DoesNotExist:
                pass
        if len(data) == 0:
            messages.success(request, "No hay turnos en la zona")
        return render(request, self.template_name, {'turnos': data})


class ListCovid(View):
    template_name = "listVaccines/listCovid.html"

    vacuna = Vaccine.objects.filter(name="COVID").first()
    if vacuna == None:
        vacuna = Vaccine.objects.create(name="COVID", timeSpan=21)
        vacuna = Vaccine.objects.filter(name="COVID").first()

    def get(self, request, *args, **kwargs):
        id_covid=Vaccine.objects.get(name = "COVID")
        data=[]
        turns=Turn.objects.order_by("date").filter(vaccine_id = id_covid)

        for t in turns:
            try:
                    if (t.date < date.today() or t.status==True):
                        turn=t
                        turn.vaccine_id="COVID"
                        turn.user_id=User.objects.get(id = t.user_id)
                        turn.zone=turn.user_id.zone
                        data.append(turn)
            except Turn.DoesNotExist:
                pass
        if len(data) == 0:
            messages.success(request, "No hay historial de turnos de tipo Covid")

        return render(request, self.template_name, {'turnos': data})

class ListGripe(View):
    template_name = "listVaccines/listGripe.html"

    def get(self, request, *args, **kwargs):
        id_covid=Vaccine.objects.get(name = "GRIPE")
        data=[]
        turns=Turn.objects.order_by("date").filter(vaccine_id = id_covid)

        for t in turns:
            try:
                    if (t.date < date.today() or t.status==True):
                        turn=t
                        turn.vaccine_id="GRIPE"
                        turn.user_id=User.objects.get(id = t.user_id)
                        turn.zone=turn.user_id.zone
                        data.append(turn)
            except Turn.DoesNotExist:
                pass
        if len(data) == 0:
            messages.success(request, "No hay historial de turnos de tipo Gripe")

        return render(request, self.template_name, {'turnos': data})


class ListVaccination(View):
    template_name = "listVaccination.html"
    



    def get(self, request, *args, **kwargs):

        data=Information.objects.all()
        if data.exists() == False:
            data=Information.objects.create(name="Vacunatorio 1", email="Vacunatorio1@gmail.com",tel=12345,description="")
            data=Information.objects.create(name="Vacunatorio 2", email="Vacunatorio2@gmail.com",tel=12345,description="")
            data=Information.objects.create(name="Vacunatorio 3", email="Vacunatorio3@gmail.com",tel=12345,description="")


        data=Information.objects.all()
        return render(request, self.template_name, {'vacunatorios': data})


def modificar_vacunatorio(request, id):  

    vaccination=Information.objects.get(id=id)

    data={
        'form':informationRegForm(instance=vaccination)
    }

    if request.method == 'POST':
        formulary=informationRegForm(data=request.POST,instance=vaccination)
        if formulary.is_valid():
            formulary.save()
            messages.success(request, "Se modifico el vacunatorio exitosamente")
            return redirect(to='main:Listar_Vacunatorios')



    return render(request,"modification/changeVaccination.html",data)



###COMO SE LLAMA A AMARILLA?  Y SE ROMPE CUANDO NO EXISTE LA VACUNA
class ListAmarilla(View):
    template_name = "listVaccines/listAmarilla.html"


    def get(self, request, *args, **kwargs):
        id_covid=Vaccine.objects.get(name = "AMARILLA")
        data=[]
        turns=Turn.objects.order_by("date").filter(vaccine_id = id_covid)

        for t in turns:
            try:
                    if (t.date < date.today()):
                        turn=t
                        turn.vaccine_id="AMARILLA"

                        turn.user_id=User.objects.get(id = t.user_id)
                        turn.zone=turn.user_id.zone
                        data.append(turn)
            except Turn.DoesNotExist:
                pass
        if len(data) == 0:
            messages.success(request, "No hay historial de turnos de tipo Fiebre amarilla")

        return render(request, self.template_name, {'turnos': data})

class Info(View):
    template_name = "info.html"

    


    def get(self, request, *args, **kwargs):
<<<<<<< HEAD

        data=Information.objects.all()
        if data.exists() == False:
            data=Information.objects.create(name="Vacunatorio 1", email="Vacunatorio1@gmail.com",tel=12345,description="")
            data=Information.objects.create(name="Vacunatorio 2", email="Vacunatorio2@gmail.com",tel=12345,description="")
            data=Information.objects.create(name="Vacunatorio 3", email="Vacunatorio3@gmail.com",tel=12345,description="")

=======
        
        
>>>>>>> 530f9fd125bc02afb9e05a368d41ab20151ee500
        data=Information.objects.all()
    
        return render(request, self.template_name, {'informacion': data})

class ListTurnRequests(View):
    template_name = "listTurnRequestAM.html"
    

    def get(self, request, *args, **kwargs):
        users = User.objects.select_related()
        turnR = Turn.objects.filter(date = None, accepted = False)
        aux = []
        for t in turnR:
            aux.append(User.objects.filter(id = t.user_id).first())
        #print(aux)
        if len(aux) == 0:
            messages.error(request, "No hay solicitudes pendientes.")
        return render(request, self.template_name, {'usuarios': aux})

    def post(self, request, *args, **kwargs):
        request.session['arg_user_id'] = request.POST["usuario_id"]
        #print(request.POST)
        try:
            if request.POST.get('arg_btn_denegar') == "True":
                pass
                #ELIMINAR TURNO

                Turn.objects.filter(user_id = request.POST["usuario_id"], date = None).delete()
            
                messages.success(request, "Operación exitosa.")
                return redirect(reverse_lazy('main:Listar_solicitudes'))
            if request.POST.get('arg_btn_asignar') == "True":
                return redirect(reverse_lazy('main:Aceptar_solicitud'))
        except KeyError:
            pass
        #print('/'*20)
        #request.session['date'] = datetime.today().date().__str__()
        #print(request.session['date'])
        #print('/'*20)
        return redirect(reverse_lazy('main:Aceptar_solicitud'))

class SetTurnRequestDate(View):
    template_name = "setTurnRequestDate.html"
    #form_class =
    success_url = reverse_lazy('main:Listar_solicitudes')

    def get(self,request, *args, **kwargs):
        print(request.session.get('arg_user_id'))
        today_d = datetime.today().date().__str__()
        return render(request, self.template_name, {'date_d':today_d})

    def post(self, request, *args, **kwargs):
        #print('/'*20) 
        #print(request.session.get('arg_user_id'))
        #print('/'*20)
        #print(request.POST['dateOfBirth'])

        turn = Turn.objects.filter(user_id = request.session.get('arg_user_id'), date = None).first()

        turn.date = datetime.fromisoformat(request.POST['dateOfBirth'])
        turn.accepted = True
        turn.save()
        print(turn.id)

        return redirect(self.success_url)


class FormularioDeIngreso(View):
    template_name = "formulary.html"
    form_class = FormularioDeIngresoForm
    success_url = reverse_lazy('main:homeS')
    
    def sacarEdad(self,user):
        fecha1 = user.dateOfBirth
        #fecha2 = date.today()
        #edad = fecha2.year - fecha1.year - 1
        #if fecha2.month >= fecha1.month:
        #    if fecha2.day >= fecha1.day:
        #        edad = edad + 1
        edad = relativedelta(datetime.now(), fecha1)
        return edad.years 

    def asignar_turno_gripe(self,usuario):
        formulario1 = Formulary.objects.filter(user = usuario).first()
        if formulario1 == None:
            return ValueError("ESTE USUARIO NO COMPLETO EL FORMULARIO DE INGRESO")
            return "ESTE USUARIO NO COMPLETO EL FORMULARIO DE INGRESO"
        if formulario1.gripe_date != None:
            if formulario1.gripe_date.__add__(timedelta(days=365)).__gt__(date.today()):
                vacuna = Vaccine.objects.filter(name="GRIPE").first()
                if vacuna == None:
                    vacuna = Vaccine.objects.create(name="GRIPE", timeSpan=12.24)
                    vacuna = Vaccine.objects.filter(name="GRIPE").first()
                
                fechaFinal = formulario1.admissionDate.__add__(timedelta(days=365))
                Turn.objects.create(user = usuario, vaccine = vacuna, status = False, date = fechaFinal)
                print(f'///GRIPE/// - PLAZO ///NO/// CUMPLIDO - {formulario1.admissionDate} (HOY) ---> {fechaFinal}')
                return "Turno GRIPE creado con exito"

                return ValueError("ESTE USUARIO SE APLICO LA VACUNA DE LA GRIPE HACE MENOS DE UN ANIO")
                return "ESTE USUARIO SE APLICO LA VACUNA DE LA GRIPE HACE MENOS DE UN ANIO"
  
        de_riesgo = formulario1.risk

        if self.sacarEdad(usuario) > 60 or (self.sacarEdad(usuario) < 60 and de_riesgo):
            fechaFinal = formulario1.admissionDate.__add__(timedelta(weeks=12))
            print(f'///GRIPE/// - GRUPO DE RIESGO - {formulario1.admissionDate} (HOY) ---> {fechaFinal}')
        else: 
            if self.sacarEdad(usuario) < 60:
                fechaFinal = formulario1.admissionDate.__add__(timedelta(weeks=26))
                print(f'///GRIPE/// - GRUPO NORMAL - {formulario1.admissionDate} (HOY) ---> {fechaFinal}')
    
        vacuna = Vaccine.objects.filter(name="GRIPE").first()
        if vacuna == None:
            vacuna = Vaccine.objects.create(name="GRIPE", timeSpan=12.24)
            vacuna = Vaccine.objects.filter(name="GRIPE").first()
            
        Turn.objects.create(user = usuario, vaccine = vacuna, status = False, date = fechaFinal)

        return "Turno GRIPE creado con exito"
            
    def asignar_turno_covid(self,edad,de_riesgo, cant_dosis_dadas,usuario,admissionDate=None,fecha_primera_dosis = None):
            #admissionDate se ingresa si el metodo se llama desde la creacion del formulario

            if edad < 18:
                return ValueError("No deberia asignar un turno(COVID) a un menor de 18")

            if cant_dosis_dadas != None: #solicitar nro de dosis aplicadas al modelo
                dias = 0
                rango_edades = list(range(18,61))
                vacuna = Vaccine.objects.filter(name="COVID")
                vacuna = vacuna.first()
                if vacuna == None:
                    #print(vacuna)
                    vacuna = Vaccine.objects.create(name="COVID",timeSpan=21)
                    vacuna = Vaccine.objects.filter(name="COVID")
                    vacuna = vacuna.first()
                
                fecha = date.today()

                if cant_dosis_dadas == 0:
                    if (edad in rango_edades and de_riesgo) or edad > 60:
                        dias = 7                    
                        fecha = admissionDate.__add__(timedelta(dias))
        
                        turno = Turn.objects.create(user = usuario, vaccine = vacuna, status = False, date = fecha)
                        return f"GRUPO DE RIESGO - 0/2 dosis - {admissionDate} (HOY) ---> {fecha}"
                    if edad in rango_edades and not de_riesgo:
                        dias = 21                 
                        fecha = admissionDate.__add__(timedelta(dias))

                        turno = Turn.objects.create(user = usuario, vaccine = vacuna, status = False, date = fecha)
                        return f"GRUPO NORMAL - 0/2 dosis - {admissionDate} (HOY) ---> {fecha}"

                if cant_dosis_dadas == 1:
                    fecha_primera_dosis = date.fromisoformat(fecha_primera_dosis)
                    #fechaAUX = fechaAUX.__add__(timedelta(22))
                    #print(fecha_primera_dosis)
                    #print(fecha_primera_dosis.__add__(timedelta(21)))

                    if fecha_primera_dosis.__add__(timedelta(21)).__lt__(date.today()): #si ya pasaron 21 dias
                        fecha_primera_dosis = admissionDate

                        if (edad in rango_edades and de_riesgo) or edad > 60:
                            dias = 7                     
                            fechaFinal = fecha_primera_dosis.__add__(timedelta(dias))
                            #turnoAUX = Turn(usuario,vacuna,False,fecha)
                            #turnoAUX.save()
                            turno = Turn.objects.create(user = usuario, vaccine = vacuna, status = False, date = fechaFinal)
                            return f"GRUPO DE RIESGO - PLAZO CUMPLIDO - 1/2 dosis - {fecha_primera_dosis} (HOY) ---> {fechaFinal}"

                        if edad in rango_edades and not de_riesgo:
                            dias = 21                  
                            fechaFinal = fecha_primera_dosis.__add__(timedelta(dias))

                            turno = Turn.objects.create(user = usuario, vaccine = vacuna, status = False, date = fechaFinal)
                            return f"GRUPO NORMAL - PLAZO CUMPLIDO - 1/2 dosis - {fecha_primera_dosis} (HOY) ---> {fechaFinal}"
                        
                    else: #si NO pasaron 21 dias
                        dias = 21                 
                        fechaFinal = admissionDate.__add__(timedelta(dias))

                        if (edad in rango_edades and de_riesgo) or edad > 60:           
                            turno = Turn.objects.create(user = usuario, vaccine = vacuna, status = False, date = fechaFinal)
                            return f"GRUPO DE RIESGO - PLAZO ///NO/// CUMPLIDO - {admissionDate} (HOY) ---> {fechaFinal}"

                        if edad in rango_edades and not de_riesgo:                    
                            turno = Turn.objects.create(user = usuario, vaccine = vacuna, status = False, date = fechaFinal)
                            return f"GRUPO NORMAL - PLAZO ///NO/// CUMPLIDO - {admissionDate} (HOY) ---> {fechaFinal}"

                if cant_dosis_dadas == 2:
                    return ["2","USUARIO 2/2 dosis (NO se asignó turno)"]

            return 1

    

    def get(self, request, *args, **kwargs):
        #print(request.user.id)
        user = User.objects.filter(id = request.user.id)
        user = user.first()
        if user != None:
            #print("Usuario existe")
            formulary1 = Formulary.objects.filter(user_id = request.user.id)
            formulary1 = formulary1.first()
            if formulary1 != None:
                #print(formulary1)
                #print('Tengo formulario')
                return redirect(self.success_url)
            else:
                #print("NO tengo formulario") 
                return render(request, self.template_name, {'form': self.form_class})

        return render(request, self.template_name, {'form': self.form_class}) # POR LAS DUDAS

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        #print(form.data)
        if form.is_valid():
            #print('is_valid')
            user = User.objects.filter(id = request.user.id)
            if user.exists():
                user = user.first()
                cant = 0

                if form.data["covid_1_date"] != "":
                    cant = cant + 1
                    fecha_primera_dosis =  date.fromisoformat(form.data["covid_1_date"])
                    C1D = date.fromisoformat(form.data["covid_1_date"])
                else:
                    C1D = None

                if form.data["covid_2_date"] != "":
                    cant = cant + 1
                    C2D = date.fromisoformat(form.data["covid_2_date"])
                else:
                    C2D = None
                
                try:
                    if form.data["de_riesgo"] == 'on':
                        de_riesgo = True
                except KeyError:
                    de_riesgo = False

                try:
                    if form.data["amarilla_ok"] == 'on':
                        amarilla = True
                except KeyError:
                    amarilla = False

                if form.data["gripe_date"] != "":
                    GD = date.fromisoformat(form.data["gripe_date"])
                else:
                    GD = None
                
                edad = self.sacarEdad(user)
                fechaDeHoy = date.today()


                
                Formulary.objects.create(
                    user = user,
                    risk = de_riesgo, 
                    admissionDate = fechaDeHoy,
                    covid_1_date = C1D,
                    covid_2_date = C2D,
                    gripe_date = GD,
                    amarilla_ok = amarilla
                )
                try:
                    print(self.asignar_turno_gripe(user))
                except ValueError:
                    messages.error(request, "No se le asignó un turno para la vacuna de la gripe, porque no pasó un año desde su última dosis.")
                    
                if form.data["covid_1_date"] == "" and form.data["covid_2_date"] != "":
                    try: 
                        print(self.asignar_turno_covid(edad,de_riesgo,cant,user,fechaDeHoy,form.data["covid_2_date"]))
                        messages.success(request, "Envío de formulario exitoso.")

                        return redirect(self.success_url)
                    except ValueError:
                        messages.error(request, "No se puede asignar un turno para la vacuna de covid a usuarios menores de edad")
                        return render(request, self.template_name, {'form':self.form_class})
                    

                if form.data["covid_2_date"] == "" and form.data["covid_1_date"] != "":

                    try: 
                        print(self.asignar_turno_covid(edad,de_riesgo,cant,user,fechaDeHoy,form.data["covid_1_date"]))
                        messages.success(request, "Envío de formulario exitoso.")
                        return redirect(self.success_url)
                    except ValueError:
                        messages.error(request, "No se puede asignar un turno para la vacuna de covid a usuarios menores de edad")
                        return render(request, self.template_name, {'form':self.form_class}) 

                if form.data["covid_2_date"] != "" and form.data["covid_1_date"] != "":
                    try:                         
                        print(self.asignar_turno_covid(edad,de_riesgo,cant,user,fechaDeHoy))
                        messages.error(request, "No se le asignó un turno para la vacuna de covid ya que tiene las dos dosis.")
                        messages.success(request, "Envío de formulario exitoso.")
                        return redirect(self.success_url)
                    except ValueError:
                        messages.error(request, "No se puede asignar un turno para la vacuna de covid a usuarios menores de edad")
                        return render(request, self.template_name, {'form':self.form_class}) 
                
                if form.data["covid_2_date"] == "" and form.data["covid_1_date"] == "":
                    try:                         
                        print(self.asignar_turno_covid(edad,de_riesgo,cant,user,fechaDeHoy))
                        messages.success(request, "Envío de formulario exitoso.")
                        return redirect(self.success_url)
                    except ValueError:
                        messages.error(request, "No se puede asignar un turno para la vacuna de covid a usuarios menores de edad")
                        return render(request, self.template_name, {'form':self.form_class}) 

            return redirect(self.success_url)
            
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form':form})

    



"""if zoneFilter == None:
            turns=Turn.objects.all()

            for t in turns:
                try:
                    aux=t
                    aux.vaccine_id=Vaccine.objects.get(id = aux.vaccine_id)
                    aux.user_id=User.objects.get(id = aux.user_id)
                    data.append(aux)
                except Turn.DoesNotExist:
                    pass

        else:"""