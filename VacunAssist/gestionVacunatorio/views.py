import argparse
from ast import If
from inspect import ArgSpec
import django
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django import forms
from django.forms import ModelForm
from .models import Vaccinator 
# Create your views here.


def saludo(request):
    return render(request, 'prueba.html')


def home(request):
    return render(request,'home.html')


def forum(request):
    return HttpResponse('Forum')

def logIn(request):
    return HttpResponse('Log In')

def signIn(request):
    return HttpResponse('Sign In')