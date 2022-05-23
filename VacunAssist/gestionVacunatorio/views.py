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
from .forms import UserLoginForm, UserRegForm, ChangeUserPasswordForm
from .models import Vaccinator, User
from .mail.send_email import *

def saludo(request):
    return render(request, 'prueba.html')

def home(request):
    return render(request,'home.html')

class UserRegistration(CreateView):
    model = User
    form_class = UserRegForm
    template_name = 'registration/user_registration.html'
    success_url = reverse_lazy('main:Inicio_de_sesion')

class UserLogin(FormView):
    template_name = "login/user_login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy('main:Saludo')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(UserLogin,self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(UserLogin, self).form_valid(form)

class ChangeUserPassword(View):
    template_name = "modification/changePass.html"
    form_class = ChangeUserPasswordForm
    success_url = reverse_lazy('main:Saludo') #cambiar

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
                return redirect(self.success_url)

            return redirect(self.success_url)
            
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form':form})
            










 
"""
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(ChangeUserPassword,self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        #
        return super(ChangeUserPassword, self).form_valid(form)

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
    

