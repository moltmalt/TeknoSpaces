from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin  # Kani kay ga cutom user admin ko 
from .models import Space

class AdminSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Admin  #from admin model ako ni gikuha 
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['space_title', 'description', 'location', 'from_date', 'to_date', 
                  'seating_capacity', 'has_air_conditioner', 'has_internet', 'has_television']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }
