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
from .forms import UserLoginForm, UserRegForm
from .models import Vaccinator, User 

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


    

