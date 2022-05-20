from django.forms import CharField, ModelForm, PasswordInput,EmailInput, IntegerField, TextInput, ChoiceField
from .models import *
from django.contrib.auth.forms import AuthenticationForm


class UserRegForm(ModelForm):
    password1 = CharField(label='Contraseña', widget = PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password1',
                'required': 'required',
            }
        )
    )

    password2 = CharField(label='Contraseña de confirmacion', widget = PasswordInput(
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
        ("Cementerio","Cementerio")
        ]

        genders = [
        ("Masculino","Masculino"),
        ("Femenino","Femenino"),
        ("Otro","Otro")
        ]

        model = User
        fields = {'dni','name','surname','email','dateOfBirth', 'zone',  'gender'}
        """widgets = {
            'dni': IntegerField(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Dni',
                }
            ),
            'name': TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                }
            ),
            'surname': TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Apellido',
                }
            ),
            'email': EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Email',
                }
            ),
            'dateOfBirth':EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Fecha de nacimiento',
                }
            ),
            'zone':ChoiceField(
                #zones,
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Zona',
                }
            ),
            'gender':ChoiceField(
                genders,
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Genero',
                }
            ),

        }"""


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
        
