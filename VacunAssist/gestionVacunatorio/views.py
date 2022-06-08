from queue import Empty
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from .models import UserManager
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import Vaccinator, User
from .mail.send_email import *
from django.contrib import messages


def saludo(request):
    return render(request, 'prueba.html')

def home(request):
    return render(request,'indexHome.html')

def homeAdmin(request):
    return render(request,'homeAdmin.html')


def homeWithSession(request):
    return render(request,'homeWithSession.html')

def vaccinatorManager(request):
    return render(request,'vaccinatorsManager.html')

class UserRegistration(CreateView):
    model = User
    form_class = UserRegForm
    template_name = 'registration/signIn.html'
    success_url = reverse_lazy('main:Inicio_de_sesion')

class VaccinatorRegistration(CreateView):
    model = Vaccinator
    form_class = VaccinatorRegForm
    template_name = 'registration/registerVaccinator.html'
    success_url = reverse_lazy('main:Inicio_de_sesion_staff')

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
        messages.success(self.request,"Inicio de sesion exitoso")
        return super(UserLogin, self).form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


def custom_logout(request):
    print('Loggin out {}'.format(request.user))
    logout(request)
    print(request.user)
    return render(request,'indexHome.html')


#Eso nose de donde salio

"""  @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(ChangeUserPassword,self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        return super(ChangeUserPassword, self).form_valid(form)
"""


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
    template_name = 'registration/user_registration.html'
    success_url = reverse_lazy('main:homeA')


"""class ChangeUserEmail(View):
    template_name = "modification/changeUserEmail.html"
    form_class = ChangeUserEmailForm
    success_url = reverse_lazy('main:homeS') #CAMBIAR

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(id = request.user.id)
            if user.exists():
                user = user.first()
                user.set_new_email(form.cleaned_data.get('email1'))
                user.save()
                return redirect(self.success_url)

            return redirect(self.success_url)
            
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form':form })

 """

class staffLogin(FormView):
    template_name = "login/staff_login.html"
    form_class = VaccinatorLoginForm
    success_url = reverse_lazy('main:homeA')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args,**kwargs):
        if len(request.POST) != 0:
            print(request.POST['username'])
            try:
                if (request.POST['username']== "admin"):
                    m= Admin.objects.get(name=request.POST['username'])
                else:
                    m = Vaccinator.objects.get(email=request.POST['username'])
                if m.check_password(request.POST['password']):
                    request.session['id'] = m.id
                    messages.success(self.request,"Contraseña correcta")
                    return HttpResponseRedirect(self.get_success_url())
                else:
                    messages.error(self.request,"Contraseña incorrecta")
            except Vaccinator.DoesNotExist:
                messages.error(self.request,"contraseña incorrecta")
        return super(staffLogin,self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request,"Inicio de sesion exitoso")
        return super(staffLogin, self).form_valid(form)

    
    def form_invalid(self, form):
        return super().form_invalid(form)

"""
class DeleteVaccinator(View):
    template_name = "modification/deleteVaccinator.html"
    form_class = DeleteVaccinatorForm
    success_url = reverse_lazy('main:homeS') #CAMBIAR
    denied_url = reverse_lazy('main:Eliminar_Vacunador')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            vaccdni = form.cleaned_data.get('vaccinator1')
            user = Vaccinator.objects.filter(dni=vaccdni)
            if user.exists():
                user.delete()
            else: 
                messages.info(request,'El DNI ingresado no se encuentra en el sistema') 
                redirect(self.denied_url) 
            return redirect(self.denied_url)         
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form':form })


def list_vaccinator(request):
    vaccinator = Vaccinator.objects.all()
    data = {
        'vaccinator': vaccinator
    }
    return render(request, "listVaccinators.html", data)                                                         

def changePassword(request):
    if request.method == "POST":
        form = changeUserPasswordForm(request.POST)
        print(request.POST)
        print('0'*20)
        if form.is_valid():
            print('1'*20)
            data = request.POST["email"]
            user = User.objects.get(email=data)
            if user is not None:
                print('2'*20)
                user.password = request.POST["password"]
                user.save()
                sendchangePassword(user.email,user.name)
                return render(request,'home.html')
    form = changeUserPasswordForm()
    return render(request,"modification/changePass.html", {'form':form})
"""
    

