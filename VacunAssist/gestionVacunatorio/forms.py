from dataclasses import fields
from django.contrib.auth.forms import ModelForm
from .models import User

class UserForm(ModelForm):
    class Meta: 
        model = User
        fields = ('name','surname','dni','dateOfBirth','zone','email','password','genre')
