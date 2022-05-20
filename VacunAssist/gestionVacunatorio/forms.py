from dataclasses import fields
from django.forms import CharField, ModelForm, PasswordInput
from .models import *
from django.contrib.auth.forms import AuthenticationForm


class UserRegForm(ModelForm):
    password1 = CharField(label='Contraseña', widget = PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password1'
                'required': 'required',
            }
        )
    )

    password1 = CharField(label='Contraseña de confirmacion', widget = PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password1'
                'required': 'required',
            }
        )
    )

"""class UserRegForm(ModelForm):
    class Meta: 
        model = User
        fields = ('name','surname','dni','dateOfBirth','zone','email','password','gender')
        
        #fields = '__all__'

class SecondFactor_UserRegForm(ModelForm):
    class Meta: 
        model = User
        #fields = ('name','surname','dni','dateOfBirth','zone','email','password','gender')
        
        fields = '__all__'"""



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
        
