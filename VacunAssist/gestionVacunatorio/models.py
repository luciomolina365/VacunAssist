import email
from os import F_OK
from turtle import title
from django.db import models

# Create your models here.


class User(models.Model):

    zones = [
        ("Terminal de ómnibus","Terminal de ómnibus"), 
        ("Municipalidad de La Plata","Municipalidad de La Plata"),
        ("Cementerio","Cementerio")
    ]

    genders = [
        ("Masculino","Masculino"),
        ("Femenino","Femenino"),
        ("Otro","Otro")
    ]
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=30, null=False)
    surname=models.CharField(max_length=30)
    dni=models.IntegerField()
    dateOfBirth=models.DateField()
    zone=models.CharField(max_length=30 , choices = zones)
    email=models.CharField(max_length=30)
    secondFactor=models.IntegerField()
    gender=models.CharField(max_length=30 , choices = genders)


class Vaccinator(models.Model):
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    dni=models.IntegerField()
    email=models.CharField(max_length=30)

class Admin(models.Model):
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=30,null=False)

class Formulary(models.Model):
    user = models.ForeignKey("gestionVacunatorio.User", on_delete=models.CASCADE)
    risk=models.BooleanField()
    admissionDate=models.DateField()


class Vaccine(models.Model):
    name=models.CharField(max_length=30)
    timeSpan=models.IntegerField()

class AplicatedVaccine(models.Model):
    dose = [ (1,1),(2,2)]

    formulary = models.ForeignKey("gestionVacunatorio.Formulary", on_delete=models.CASCADE)
    vaccine = models.ForeignKey("gestionVacunatorio.Vaccine", on_delete=models.CASCADE)
    doseNumber=models.IntegerField(choices = dose, blank=True)
    aplicationDate=models.DateField()

class Turn(models.Model):
    user = models.ForeignKey("gestionVacunatorio.User", on_delete=models.CASCADE)
    vaccine = models.ForeignKey("gestionVacunatorio.Vaccine", on_delete=models.CASCADE)
    status=models.BooleanField()
    date=models.DateField()

class Forum(models.Model):
    user=models.CharField(max_length=30,null=False)
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    date=models.DateField()
