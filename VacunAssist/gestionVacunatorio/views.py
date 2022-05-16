from django.shortcuts import render, HttpResponse
from django.views.generic import View

from .forms import UserRegForm

from .models import Vaccinator, User 

def saludo(request):
    return render(request, 'prueba.html')


def home(request):
    return render(request,'home.html')


"""class UserRegistration(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, "registration/user_registration.html", {"form": form})


    def post(self, request):
        pass"""

def userRegistration(request):
    if request.method == "POST":
        form = UserRegForm(request.POST)
        print(form)
    return render(request, "registration/user_registration.html")



    


def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')