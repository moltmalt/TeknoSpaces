from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin

class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ['username', 'password1', 'password2']
