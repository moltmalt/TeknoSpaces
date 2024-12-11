from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'class': 'w-full h-12 border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'w-full h-12 border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2',
    }))

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.status == 'inactive':
            raise forms.ValidationError(
                _("This account is inactive."),
                code='inactive',
            )

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'class': 'w-full h-12 border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'w-full h-12 border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2',
    }))