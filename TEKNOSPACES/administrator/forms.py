from django import forms
from .models import User, Space
from django.core.exceptions import ValidationError


class UserSignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)  # Create the user instance pero aysa isave nana unya
        user.set_password(self.cleaned_data['password1']) 
        if commit:
            user.save()  
        return user

class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['space_title', 'description', 'location', 'from_date', 'to_date', 
                  'seating_capacity', 'has_air_conditioner', 'has_internet', 'has_television']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date and to_date and from_date > to_date:
            raise ValidationError("To date cannot be earlier than From date.")
