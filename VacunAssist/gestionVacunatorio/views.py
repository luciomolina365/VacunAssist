from django.http import QueryDict
from django.shortcuts import render, HttpResponse
from django.views.generic import View
import random
import copy

from .forms import SecondFactor_UserRegForm, UserRegForm

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

        if form.is_valid():

            number = random.randint(0000,9999)
            form.cleaned_data['secondFactor'] = number
            data = form.cleaned_data
            print(data)
            form2 = SecondFactor_UserRegForm(data)
            
            form2.save()

            
            return render(request,'home.html')

    form = UserRegForm    
    return render(request, "registration/user_registration.html", {'form':form})



    


def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')