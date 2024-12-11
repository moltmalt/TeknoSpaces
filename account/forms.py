from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'first_name', 'last_name', 'email']  # Only editable fields
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    # Fields not required in the form but still need to be preserved
    sex = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    usertype = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    program = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        # Save the form as usual
        instance = super().save(commit=False)

        # If these fields were not changed, keep their original values
        if not self.cleaned_data.get('sex'):
            instance.sex = self.instance.sex
        if not self.cleaned_data.get('usertype'):
            instance.usertype = self.instance.usertype
        if not self.cleaned_data.get('program'):
            instance.program = self.instance.program
        if not self.cleaned_data.get('status'):
            instance.status = self.instance.status

        if commit:
            instance.save()

        return instance