from django import forms
from datetime import datetime
from .models import Space

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class EditSpaceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to fields
        for field_name, field in self.fields.items():
            if field_name in ['title', 'description', 'price', 'venue', 'seating_capacity', 'category', 'type', 'book_count', 'managed_by', 'booked_by', 'is_booked']:
                field.widget.attrs.update({
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
                })
            elif field_name in ['hasAirConditioner', 'hasInternet', 'hasTelevision']:
                field.widget.attrs.update({
                    'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
                })

    class Meta:
        model = Space

        fields = [
            'main_image', 'second_image', 'third_image', 'fourth_image',
            'fifth_image', 'sixth_image', 'title', 'description', 'price',
            'booked_by', 'is_booked', 'venue', 'seating_capacity', 'managed_by',
            'hasAirConditioner', 'hasInternet', 'hasTelevision', 'category', 'type'
        ]

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'w-full py-2 px-4 rounded-lg border border-gray-300',
                'rows': 4
            }),
            'main_image': forms.ClearableFileInput(attrs={'class': 'w-full py-2'}),
            'second_image': forms.ClearableFileInput(attrs={'class': 'w-full py-2'}),
            'third_image': forms.ClearableFileInput(attrs={'class': 'w-full py-2'}),
            'fourth_image': forms.ClearableFileInput(attrs={'class': 'w-full py-2'}),
            'fifth_image': forms.ClearableFileInput(attrs={'class': 'w-full py-2'}),
            'sixth_image': forms.ClearableFileInput(attrs={'class': 'w-full py-2'}),
            'title': forms.TextInput(attrs={'class': 'w-full py-2 px-4 rounded-lg border border-gray-300'}),
            'price': forms.NumberInput(attrs={'class': 'w-full py-2 px-4 rounded-lg border border-gray-300'}),
            'booked_by': forms.Select(attrs={'class': 'w-full py-2 px-4 rounded-lg border border-gray-300'}),
            'maanged_by': forms.Select(attrs={'class': 'w-full py-2 px-4 rounded-lg border border-gray-300'}),
            'is_booked': forms.CheckboxInput(attrs={'class': 'h-5 w-5'}),
            'venue': forms.TextInput(attrs={'class': 'w-full py-2 px-4 rounded-lg border border-gray-300'}),
            'seating_capacity': forms.NumberInput(attrs={'class': 'w-full py-2 px-4 rounded-lg border border-gray-300'}),
            'hasAirConditioner': forms.CheckboxInput(attrs={'class': 'h-5 w-5'}),
            'hasInternet': forms.CheckboxInput(attrs={'class': 'h-5 w-5'}),
            'hasTelevision': forms.CheckboxInput(attrs={'class': 'h-5 w-5'}),
        }
        
        labels = {
            'main_image': 'Main Image',
            'second_image': 'Second Image',
            'third_image': 'Third Image',
            'fourth_image': 'Fourth Image',
            'fifth_image': 'Fifth Image',
            'sixth_image': 'Sixth Image',
            'title': 'Title',
            'description': 'Description',
            'price': 'Price',
            'booked_by': 'Booked By',
            'managed_by': 'Managed By',
            'is_booked': 'Is Booked',
            'venue': 'Venue',
            'seating_capacity': 'Seating Capacity',
            'hasAirConditioner': 'Air Conditioner',
            'hasInternet': 'Internet',
            'hasTelevision': 'Television',
        }


class SpaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to fields
        for field_name, field in self.fields.items():
            if field_name in ['title', 'description', 'price', 'venue', 'seating_capacity', 'category', 'type']:
                field.widget.attrs.update({
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
                })
            elif field_name in ['hasAirConditioner', 'hasInternet', 'hasTelevision']:
                field.widget.attrs.update({
                    'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
                })
    class Meta:
        model = Space
        fields = '__all__'