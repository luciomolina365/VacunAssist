from django.shortcuts import render, HttpResponse

# Create your views here.


def saludo(request):
    return render(request , 'prueba.html')


def home(request):
    return render(request,'home.html')


def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')