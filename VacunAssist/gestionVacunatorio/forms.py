from dataclasses import fields
from django.forms import ModelForm
from .models import User

class UserRegForm(ModelForm):
    class Meta: 
        model = User
        fields = ('name','surname','dni','dateOfBirth','zone','email','password','gender')
