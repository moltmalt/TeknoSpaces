from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin  # If you are using a custom Admin model

class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Admin  # Make sure Admin is correctly defined or replace with User if not custom
        fields = ['username', 'password1', 'password2']
