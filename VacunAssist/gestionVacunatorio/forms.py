from genericpath import exists
from django import forms
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
import string
from .mail.send_email import *
from datetime import date
from django.core.exceptions import ValidationError


#-------------------------------------------------------------------------
##USER

class UserLoginForm(AuthenticationForm):
    #el email se hereda del username_field del model
    default_errors = {
        "invalid_login": (
            "Ha ingresado incorrectamente alguno de los campos.\n "
            "Tenga en cuenta que la clave debe ser de 6 caracteres o mas.\n "
            "El segundo factor es de 4 digitos y la clave no posee caracteres especiales."
        )
    }

    password = forms.CharField(error_messages=default_errors ,label='Contraseña', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password',
                'required': 'required',
            }
        )
    )

    

    secondFactor = forms.IntegerField(error_messages=default_errors ,label='Segundo Factor', widget = forms.NumberInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese el nro de seguridad',
                'id':'secondFactor',
                'required': 'required',
            }
        )
    ) 


    def get_invalid_login_error(self):
        return ValidationError(
            self.default_errors["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field.verbose_name},
        )

    def clean(self):
        data = super(UserLoginForm,self).clean()
        user = authenticate(email=data['username'], password= data['password'])
        if user is not None:
            if user.secondFactor != data['secondFactor']:
                print(user.secondFactor)
                raise ValidationError("Ha ingresado incorrectamente alguno de los campos. Tenga en cuenta que la clave debe ser de 6 caracteres o mas. El segundo factor es de 4 digitos y la clave no posee caracteres especiales. ")
        return data

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
                    'type':'date',
                    'max': date.today(),
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
        number = randint(1000,9999)
        user.set_secondFactor(number)

        if commit:
            send_secondFactor_email(
                str(user.email),
                str(self.get_name()),
                str(user.secondFactor)
            )
            user.save() 
            print(user.secondFactor)
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
    def clean_name(self):
        name = self.cleaned_data['name']
        for letter in name:
            if letter not in string.ascii_letters:
                raise forms.ValidationError('El nombre no debe contener numeros ni caracteres especiales')

        return name 



class ChangeUserEmailForm(forms.Form):

    email1 = forms.EmailField(label='Nueva Email', widget = forms.EmailInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese la nueva casilla de correo',
                'id':'email1',
                'required': 'required',
            }
        )
    )  


class ChangeUserZoneForm(forms.Form):

    zones = [
        ("Terminal de ómnibus","Terminal de ómnibus"), 
        ("Municipalidad de La Plata","Municipalidad de La Plata"),
        ('Cementerio','Cementerio')
        ]

    zone = forms.ChoiceField(choices=zones)


    
    
    
#-------------------------------------------------------------------------
##Vaccinator

class VaccinatorLoginForm(AuthenticationForm):
    #el email se hereda del username_field del model


    default_errors = {
    "invalid_login": (
            "Ha ingresado incorrectamente alguno de los campos.\n "
            "Tenga en cuenta que la clave debe ser de 6 caracteres o mas.\n "
        )
    }

    password = forms.CharField(error_messages=default_errors ,label='Contraseña', widget = forms.PasswordInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese su contraseña',
                'id':'password',
                'required': 'required',
            }
        )
    )

    def get_invalid_login_error(self):
        return ValidationError(
            self.default_errors["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field.verbose_name},
        )

    def __init__(self,  *args, **kwargs):
        super(VaccinatorLoginForm,self).__init__(*args, **kwargs)

    def clean(self):
        data = super(VaccinatorLoginForm,self).clean()
        user = authenticate(email=data['username'], password= data['password'])
        if user is not None:
                raise ValidationError("Ha ingresado incorrectamente alguno de los campos. Tenga en cuenta que la clave debe ser de 6 caracteres o mas. El segundo factor es de 4 digitos y la clave no posee caracteres especiales. ")
        return data


class AdminRegForm(forms.ModelForm):

    
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

        model = Admin
        fields = ['name']
        labels = { 
            'name':'Nombre',
        }
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                }
            ),
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


    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])    

        if commit:    
            user.save() 
        return user



class VaccinatorRegForm(forms.ModelForm):

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

        model = Vaccinator
        fields = ['dni','name','surname','email','zone']
        labels = { 
            'dni':'Numero de documento',
            'name':'Nombre',
            'surname':'Apellido',
            'email': 'Correo Electronico',
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
            'zone':forms.Select(choices=zones)
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

        if commit:    
            send_password_email(
                str(user.email),
                str(self.get_name()),
                str(self.cleaned_data['password1']))
            user.save() 
        return user

    def get_name(self):
        name = self.cleaned_data['name']
        return name



#-------------------------------------------------------------------------
##FORMULARY  


class FormularioDeIngresoForm(forms.Form):
    vaccines = [("COVID","COVID"),
    ("GRIPE","GRIPE"),
    ("AMARILLA","AMARILLA"),
    ]

    de_riesgo = forms.BooleanField(required=False,label="¿Usted pertenece al grupo de riesgo?", widget = forms.CheckboxInput(
            attrs ={
                'class':'form-control',
                'placeholder': '¿Usted pertenece al grupo de riesgo?',
                'id':'de_riesgo',                
            }
        )
    )
    
    covid_1_date = forms.DateField(required=False,label="Fecha primera dosis covid", widget = forms.DateInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese la fecha de su primera dosis covid',
                'id':'covid_1_date',
                'type':'date',
                'max': date.today(),
                
            }
        )
    )

    covid_2_date = forms.DateField(required=False,label="Fecha segunda dosis covid", widget = forms.DateInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese la fecha de su segunda dosis covid',
                'id':'covid_2_date',
                'type':'date',
                'max': date.today(),
            }
        )
    )

    gripe_date = forms.DateField(required=False,label="Fecha de su última vacuna de la gripe.", widget = forms.DateInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese la fecha de su última vacuna de la gripe.',
                'id':'gripe_date',
                'type':'date',
                'max': date.today(),
                
            }
        )
    )

    amarilla_ok = forms.BooleanField(required=False,label="¿Usted tiene la vacuna para la fiebre amarilla?", widget = forms.CheckboxInput(
            attrs ={
                'class':'form-control',
                'placeholder': '¿Usted tiene la vacuna para la fiebre amarilla?',
                'id':'amarilla_ok',                
            }
        )
    )
    
    
    #def __init__(self,de_riesgo, covid_1_date, covid_2_date, gripe_date, amarilla_ok):
    #    super(FormularioDeIngresoForm,self).__init__()
    #    self.de_riesgo = de_riesgo
    #    self.covid_1_date = covid_1_date
    #    self.covid_2_date = covid_2_date
    #    self.gripe_date = gripe_date
    #    self.amarilla_ok = amarilla_ok

################
class FormularioDeIngresoFormAAA(forms.ModelForm):
    class Meta:
        vaccines = [("COVID","COVID"),
        ("GRIPE","GRIPE"),
        ("AMARILLA","AMARILLA"),
        ]

        model = Formulary 
        fields = ['risk','covid_1_date','covid_2_date','gripe_date','amarilla_ok']
        widgets = {
            'de_riesgo':forms.CheckboxInput(
                attrs ={
                    'class':'form-control',
                    'placeholder': '¿Usted pertenece al grupo de riesgo?',
                    'id':'de_riesgo',             
                }
            ),
            'covid_1_date': forms.DateInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese la fecha de su primera dosis covid',
                'id':'covid_1_date',
                'type':'date',
                'max': date.today(),

            }
            ),
            'covid_2_date': forms.DateInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese la fecha de su segunda dosis covid',
                'id':'covid_2_date',
                'type':'date',
                'max': date.today(),
                'required':False
            }
            ),
            'gripe_date':forms.DateInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese la fecha de su última vacuna de la gripe.',
                'id':'gripe_date',
                'type':'date',
                'max': date.today(),
                'required':False
                
            }
            ),
            'amarilla_ok':forms.CheckboxInput(
            attrs ={
                'class':'form-control',
                'placeholder': '¿Usted tiene la vacuna para la fiebre amarilla?',
                'id':'amarilla_ok',                
                'required':False

            }
            )

        }
#################
class FormularyRegForm(forms.ModelForm):
    class Meta: 
        model = Formulary
        #falta user
        fields = ('risk','admissionDate')

class ForumRegForm(forms.ModelForm):
    class Meta: 
        model = Forum
        fields = ('title','description',"date")
        




class informationRegForm(forms.ModelForm):

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

        model = Information
        fields = ['name','email','tel','description']
        labels = { 
            'name':'Nombre',
            'email':'Email',
            'tel':'Telefono',
            'description':'Descripcion',
        }
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Email',
                }
            ),
            'tel': forms.NumberInput(),

        }
class ChangeVacEmailForm(forms.ModelForm):
    email = forms.EmailField(label='Nueva Email', widget = forms.EmailInput(
            attrs ={
                'class':'form-control',
                'placeholder': 'Ingrese la nueva casilla de correo',
                'id':'email',
                'required': 'required',
            }
        )
    )  

class ForumRegForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ['title','description','user']
        labels = { 
            'title':'Titulo',
            'description':'Descripcion',
            'user':'Usuario',
        }
        widgets = {
            'title': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Titulo',
                }
            ),
            'description': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Descripcion',
                }
            ),
            'user': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'usuario',
                }
            ),
        }

"""
 
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
