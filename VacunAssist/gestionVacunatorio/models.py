import email
from django.db import models

# Create your models here.
class Client(models.Model):

    zones = [
        ("T","Terminal de ómnibus"), 
        ("M","Municipalidad de La Plata"),
        ("C","Cementerio")
    ]

    genres = [
        ("M","Masculino"),
        ("F","Femenino"),
        ("O","Otro")
    ]

    name=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    dni=models.IntegerField()
    dateOfBirth=models.DateField()
    zone=models.CharField(max_length=30 , choices = zones)
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    secondFactor=models.IntegerField()
    genre=models.CharField(max_length=30 , choices = genres)

class Vaccinator(models.Model):
    name=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    dni=models.IntegerField()
    email=models.CharField(max_length=30)


