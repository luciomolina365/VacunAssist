from cgitb import html
from pipes import Template
from django.http import HttpResponse
from django.template import Context, Template
from django.shortcuts import render


def saludo(request):
    return render(request , 'prueba.html')

