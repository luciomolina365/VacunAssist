
from ast import arguments
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, dni, name, surname, email, dateOfBirth, 
        zone, gender, password=None, secondFactor=None):
        for arg in arguments:
            if not arg:
                raise ValueError(f'Falta {arg}')

        user = self.model(
            dni=dni,
            name=name,
            surname=surname,
            email=email,
            dateOfBirth=dateOfBirth,
            zone=zone,
            gender=gender,
            password=password,
            secondFactor=secondFactor
        )

        user.set_password(password)
        user.save()

class User(AbstractBaseUser):

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
    dni=models.IntegerField('Dni', unique=True)
    name=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    email=models.CharField('Email', max_length=30,unique=True)
    dateOfBirth=models.DateField()
    zone=models.CharField(max_length=30 , choices = zones)
    gender=models.CharField(max_length=30 , choices = genders)
    password=models.CharField(max_length=30, null=False)
    secondFactor=models.IntegerField(blank = True, null = True)
    isActive= models.BooleanField(default=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['password', 'dateOfBirth', 'zone', 'email', 'gender']

    def  __str__(self):
        return f'{self.name}'

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True

        

    
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
