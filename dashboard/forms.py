from django import forms
from django.core.exceptions import ValidationError
from booking.models import Booking
from datetime import time

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'space', 'date', 'start_time', 'end_time', 'request_letter', 'status']
        widgets = {
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'block w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500 transition duration-300 ease-in-out',
                    'placeholder': 'Start Time'
                }
            ),
            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'block w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500 transition duration-300 ease-in-out',
                    'placeholder': 'End Time'
                }
            ),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < time(8, 0) or start_time >= time(17, 0):
            raise ValidationError('Start time must be between 8:00 AM and 5:00 PM.')
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        if end_time <= time(8, 0) or end_time > time(17, 0):
            raise ValidationError('End time must be between 8:00 AM and 5:00 PM.')
        return end_time

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Check that end_time is after start_time
        if start_time and end_time and end_time <= start_time:
            raise ValidationError('End time must be after start time.')
        return cleaned_data


class DeclineBookingForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full py-4 px-6 rounded-xl border',  # Custom styling
            'placeholder': 'Please provide a reason for declining the booking.'  # Optional placeholder
        }),
        label='',  # Remove the label for the reason field
    )