from django.http import QueryDict
from django.shortcuts import render, redirect
from django.views.generic import View
import random
import copy
from django.contrib.auth import login, logout, authenticate

from .forms import SecondFactor_UserRegForm, UserRegForm

from .models import Vaccinator, User 

def saludo(request):
    return render(request, 'prueba.html')


def home(request):
    return render(request,'home.html')


def userRegistration(request):
    
    if request.method == "POST":
        
        
        form = UserRegForm(request.POST)

        if form.is_valid():

            number = random.randint(0000,9999)
            form.cleaned_data['secondFactor'] = number
            data = form.cleaned_data
            form2 = SecondFactor_UserRegForm(data)
            
            user = form2.save()
            login(request,user)
            
            
            return redirect('')

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

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
