from django import forms
from django.core.exceptions import ValidationError
from .models import Booking

class BookingForm(forms.ModelForm):
    selected_date = forms.DateField(
        widget=forms.HiddenInput(),
        required=False  # Allow empty value
    )
    selected_slots = forms.CharField(
        widget=forms.HiddenInput(), 
        required=True
    )
    request_letter = forms.FileField(
        required=True,
        help_text="Please upload a request letter"
    )

    class Meta:
        model = Booking
        fields = ['request_letter', 'selected_date', 'selected_slots']

    def clean(self):
        """
        Additional form-wide validation
        """
        cleaned_data = super().clean()

        selected_date = self.cleaned_data.get('selected_date')
        print(f"Selected date in forms.py: {selected_date}")  # Debugging line
        if selected_date is None or selected_date == '':
            raise ValidationError("Please select a valid date.")
        
        # Validate selected slots
        selected_slots = cleaned_data.get('selected_slots')
        if not selected_slots:
            raise ValidationError("Please select at least one time slot.")
        
        # Validate request letter
        request_letter = cleaned_data.get('request_letter')
        if not request_letter:
            raise ValidationError("Please upload a request letter.")
        
        return cleaned_data