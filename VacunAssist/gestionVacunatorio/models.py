import email
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from datetime import date, timedelta

# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self, dni, name, surname, email, dateOfBirth, 
        zone, gender, password=None, secondFactor=None):

        if not dni:
            raise ValueError(f'Falta dni')

        user = self.model(
            dni=dni,
            name=name,
            surname=surname,
            email=self.normalize_email(email),
            dateOfBirth=dateOfBirth,
            zone=zone,
            gender=gender,
            password=password,
            secondFactor= randint(0000,9999)
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, dni, name, surname, email, dateOfBirth, zone, gender, password=None):
        superuser = self.create_user(
            dni=dni, 
            name=name, 
            surname=surname, 
            email=email, 
            dateOfBirth=dateOfBirth, 
            zone=zone, 
            gender=gender, 
            password=password)
        superuser.is_admin = True
        superuser.save()
        return superuser
        

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
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)


    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','surname','dni','dateOfBirth', 'zone',  'gender','password']

    def  __str__(self):
        return f'{self.name}'

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def set_secondFactor(self, number):
        self.secondFactor = number

    def set_new_name(self, name):
        self.name = name
    
    def set_new_email(self, email):
        self.email = email

    def set_new_zone(self, zone):
        self.zone = zone

    
class Vaccinator(AbstractBaseUser):
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    surname=models.CharField(max_length=30)
    dni=models.IntegerField( unique=True)
    email=models.CharField(max_length=30,unique=True)
    is_active=models.BooleanField(default=True)
    is_vaccinator=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    
    zones = [
        ("Terminal de ómnibus","Terminal de ómnibus"), 
        ("Municipalidad de La Plata","Municipalidad de La Plata"),
        ("Cementerio","Cementerio")
    ]
    zone=models.CharField(max_length=30 , choices = zones, default= "Cementerio")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','surname','dni','password']



    def  __str__(self):
        return f'{self.name}'

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True


    def is_vac(self):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Admin(AbstractBaseUser):
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=30,null=False)
    is_active=models.BooleanField(default=True)
    is_vaccinator=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=True)
    
    USERNAME_FIELD = 'name'

    def isAdmin(self):
        return self.is_admin


class Formulary(models.Model):
    user = models.ForeignKey("gestionVacunatorio.User", on_delete=models.CASCADE)
    risk = models.BooleanField()
    admissionDate = models.DateField()

    covid_1_date = models.DateField(null = True)
    covid_2_date = models.DateField(null = True)
    gripe_date = models.DateField(null = True)
    amarilla_ok = models.BooleanField(null = True, default = False)



class Vaccine(models.Model):
    name = models.CharField(max_length=30)
    timeSpan = models.IntegerField()
    description = models.CharField(default = None, null = True, max_length = 140) 

    def __str__(self) -> str:
        return str(self.name)

class Information(models.Model):
    name=models.CharField(default = None,max_length=30)
    email=models.CharField(default = None,max_length=30)
    tel=models.IntegerField(default = None)
    description=models.CharField(default = None,max_length=200)

    def set_new_name(self, name):
        self.name = name
    
    def set_new_email(self, email):
        self.email = email

    def set_new_tel(self, tel):
        self.tel = tel

    def set_new_description(self, description):
        self.description = description




class Turn(models.Model):
    user = models.ForeignKey("gestionVacunatorio.User", on_delete=models.CASCADE)
    vaccine = models.ForeignKey("gestionVacunatorio.Vaccine", on_delete=models.CASCADE)
    status = models.BooleanField()
    date = models.DateField()
    accepted = models.BooleanField(default=True)

class TurnRequest(models.Model):
    user = models.ForeignKey("gestionVacunatorio.User", on_delete=models.CASCADE)
    vaccine = models.ForeignKey("gestionVacunatorio.Vaccine", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

class Forum(models.Model):
    user=models.CharField(max_length=30,null=False)
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    date=models.DateField()
