import argparse
from ast import If
from inspect import ArgSpec
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from gestionVacunatorio.models import Client
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def saludo(request):
    return render(request, 'prueba.html')


def home(request):
    return render(request,'home.html')


class UserRegistration(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, "registration/user_registration.html", {"form": form})


    def post(self, request):
        pass

    


def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')