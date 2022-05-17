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
        print(request)
        #if form.is_valid():
            #usuario = form.save()
        return(request, "home.html")

    form = UserRegForm()    
    return render(request, "registration/user_registration.html", {'form':form})



    


def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')