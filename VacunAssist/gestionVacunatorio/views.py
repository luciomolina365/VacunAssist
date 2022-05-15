import argparse
from ast import If
from inspect import ArgSpec
from django.shortcuts import render, HttpResponse
from gestionVacunatorio.models import Client
from gestionVacunatorio.forms import RegistrationForm
# Create your views here.


def saludo(request):
    return render(request, 'prueba.html')


def home(request):
    return render(request,'home.html')


def user_registration(request):
    

    if  not request.method == "POST":  #sacar NOT
        form = RegistrationForm(request.POST)

        if form.is_valid():

            return render(request,"login.html") ##login no existe todavia
    else:
        form = RegistrationForm()


    return render(request, "user_registration.html", {"form":form})

    """response = HttpResponse()
    response["name"] = request.get["name"]
    response["surname"] = request.get["surname"]
    response["dni"] = request.get["dni"]
    response["dateOfBirth"] = request.get["dateOfBirth"]
    response["zone"] = request.get["zone"]
    response["email"] = request.get["email"]
    response["password"] = request.get["password"]
    response["password_confirm"] = request.get["password_confirm"]
    response["secondFactor"] = request.get["secondFactor"]"""


    


def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')