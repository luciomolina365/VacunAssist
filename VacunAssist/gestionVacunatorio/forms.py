from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm



class UserLoginForm(AuthenticationForm):
    #el email se hereda el username del model
    password = forms.CharField(label='Contraseña', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password',
                'required': 'required',
            }
        )
    )

    secondFactor = forms.IntegerField(label='Segundo Factor', widget = forms.NumberInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese el nro de seguridad',
                'id':'secondFactor',
                'required': 'required',
            }
        )
    ) 
    def __init__(self,  *args, **kwargs):
        super(UserLoginForm,self).__init__(*args, **kwargs)
        #print(self.fields)
        #print("111"*20 )


class UserRegForm(forms.ModelForm):

    password1 = forms.CharField(label='Contraseña', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password1',
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
        fields = ['dni','name','surname','email','dateOfBirth', 'zone',  'gender']
        labels = { 
            'dni':'Numero de documento',
            'name':'Nombre',
            'surname':'Apellido',
            'email': 'Correo Electronico',
            'dateOfBirth':'Fecha de nacimiento', 
            'zone':'Zona',
            'gender':'Genero'
        }
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

    def clean_password2(self):
        print(self.cleaned_data)
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit = True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data['password1'])        
        number = randint(0000,9999)
        user.set_secondFactor(number)

        #MAIL------------------------------------------------------
    
        if commit:
            user.save()
        return user

    

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
        
