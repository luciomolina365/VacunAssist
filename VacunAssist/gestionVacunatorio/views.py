from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from .models import UserManager
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegForm
from .models import Vaccinator, User 

def saludo(request):
    return render(request, 'prueba.html')


def home(request):
    return render(request,'home.html')


class UserRegistration(CreateView):
    model = User
    form_class = UserRegForm
    template_name = 'registration/user_registration.html'
    success_url = reverse_lazy('main:Saludo')






    

"""
def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')
"""
