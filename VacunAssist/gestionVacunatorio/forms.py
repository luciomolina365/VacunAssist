import django


from django import forms

class RegistrationForm(forms.Form):

    name = forms.CharField()
    surname = forms.CharField()
    dni = forms.IntegerField()
    dateOfBirth = forms.DateField()
    #zone = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
    secondFactor = forms.IntegerField()
    #genre = forms.CharField()