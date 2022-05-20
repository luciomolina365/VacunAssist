from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm


class UserRegForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password',
                'required': 'required',
            }
        )
    )

    password2 = forms.CharField(label='Contraseña de confirmacion', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese nuevamente su contraseña',
                'id':'password2',
                'required': 'required'
            }
        )
    )
    
    class Meta:

        zones = [
        ("Terminal de ómnibus","Terminal de ómnibus"), 
        ("Municipalidad de La Plata","Municipalidad de La Plata"),
        ('Cementerio','Cementerio')
        ]

        genders = [
        ("Masculino","Masculino"),
        ("Femenino","Femenino"),
        ("Otro","Otro")
        ]

        model = User
        fields = {'dni','name','surname','email','dateOfBirth', 'zone',  'gender'}
        widgets = {
            'dni': forms.NumberInput(),
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                }
            ),
            'surname': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Apellido',
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Email',
                }
            ),
            'dateOfBirth':forms.DateInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Fecha de nacimiento',
                }
            ),
            'zone':forms.Select(choices=zones),
            'gender':forms.Select(choices=genders),

        }


class VaccinatorRegForm(forms.ModelForm):
    class Meta: 
        model = Vaccinator
        fields = ('name','surname','dni','email','password')

class FormularyRegForm(forms.ModelForm):
    class Meta: 
        model = Formulary
        #falta user
        fields = ('risk','admissionDate')

class ForumRegForm(forms.ModelForm):
    class Meta: 
        model = Forum
        fields = ('title','description',"date")
        
