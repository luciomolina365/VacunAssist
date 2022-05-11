import email
from django.db import models

# Create your models here.
class Client(models.Model):
    name=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    dni=models.IntegerField()
    dateOfBirth=models.DateField()
    zone=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    SecondFactor=models.IntegerField()

class Vaccinator(models.Model):
    name=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    dni=models.IntegerField()
    email=models.CharField(max_length=30)