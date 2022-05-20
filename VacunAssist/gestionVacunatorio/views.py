from django.shortcuts import render, redirect
from django.views.generic import View
from .models import UserManager
from django.contrib.auth import login, logout, authenticate

from .forms import UserRegForm

from .models import Vaccinator, User 

def saludo(request):
    return render(request, 'prueba.html')


def home(request):
    return render(request,'home.html')


def userRegistration(request):
    
    if request.method == "POST":
        
        
        form = UserRegForm(request.POST)

        if form.is_valid():

            print(form)
            #user = form.save()
            manager = UserManager()
            manager.create_user()
            
            login(request,user)
            
            
            return redirect('')

        else:
            #for msg in form.error_messages:
            #    print(form.error_messages[msg])
            print("AHRELOCO-"*20)


    form = UserRegForm()    
    return render(request, "registration/user_registration.html", {'form':form})



    

"""
def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')
"""
