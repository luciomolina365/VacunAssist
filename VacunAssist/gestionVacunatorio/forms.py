from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
import string
from .mail.send_email import *


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
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')

        if len(password1) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 dígitos')

        for letter in password1:
            if letter == string.whitespace:
                raise forms.ValidationError('La contraseña no debe contener espacios')
        
        return password2

    def clean_name(self):
        name = self.cleaned_data['name']
        for letter in name:
            if letter not in string.ascii_letters:
                raise forms.ValidationError('El nombre no debe contener numeros ni caracteres especiales')

        return name

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        for letter in surname:
            if letter not in string.ascii_letters:
                raise forms.ValidationError('El apellido no debe contener numeros ni caracteres especiales') 
        return surname

    def save(self, commit = True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data['password1'])        
        number = randint(0000,9999)
        user.set_secondFactor(number)

        if commit:

            send_secondFactor_email(
                str(user.email),
                str(self.get_name()),
                str(user.secondFactor)
            )

            user.save() #mover arriba
            
            

        return user

    def get_name(self):
        name = self.cleaned_data['name']
        return name
 



class ChangeUserPasswordForm(forms.Form):

    password1 = forms.CharField(label='Nueva contraseña', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password1',
                'required': 'required',
            }
        )
    )

    password2 = forms.CharField(label='Confirmacion de contraseña', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese nuevamente su contraseña',
                'id':'password2',
                'required': 'required',
            }
        )
    )

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')

        if len(password1) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 dígitos')

        for letter in password1:
            if letter == string.whitespace:
                raise forms.ValidationError('La contraseña no debe contener espacios')
        
        return password2

class ChangeUserNameForm(forms.Form):

    name = forms.CharField(label='Nuevo Nombre', widget = forms.TextInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese el nuevo nombre',
                'id':'name',
                'required': 'required',
            }
        )
    )
    def clean_password2(self):
        name = self.cleaned_data['name']
        return name


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
        
"""
    
 
class DeleteVaccinatorForm(forms.Form)
     vacunador1 = forms.TextField(label='Vacunador a eliminar', widget = forms.TextInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese el nombre del vacunador a borrar del sistema',
                'id':'vacunador1',
                'required': 'required',
 
 
 --
 
 class AdminsLoginForm(AuthenticationForm):
    
    password = forms.CharField(label='Contraseña', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password',
                'required': 'required',
            }
        )
    )
     def __init__(self,  *args, **kwargs):
        super(AdminsLoginForm,self).__init__(*args, **kwargs)
 
 """      
