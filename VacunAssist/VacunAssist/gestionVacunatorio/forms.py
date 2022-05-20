from dataclasses import fields
from django.forms import ModelForm
from .models import *


class UserRegForm(ModelForm):
    class Meta: 
        model = User
        fields = ('name','surname','dni','dateOfBirth','zone','email','password','gender')
        
        #fields = '__all__'

class SecondFactor_UserRegForm(ModelForm):
    class Meta: 
        model = User
        #fields = ('name','surname','dni','dateOfBirth','zone','email','password','gender')
        
        fields = '__all__'



class VaccinatorRegForm(ModelForm):
    class Meta: 
        model = Vaccinator
        fields = ('name','surname','dni','email','password')

class FormularyRegForm(ModelForm):
    class Meta: 
        model = Formulary
        #falta user
        fields = ('risk','admissionDate')

class ForumRegForm(ModelForm):
    class Meta: 
        model = Forum
        fields = ('title','description',"date")
        
