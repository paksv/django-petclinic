from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from .models import Pet, PetType
from owners.models import Owner

class PetForm(forms.ModelForm):
    """Form for creating and updating Pet instances"""
    
    class Meta:
        model = Pet
        fields = ['name', 'birth_date', 'type', 'owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        owner_id = kwargs.pop('owner_id', None)
        super(PetForm, self).__init__(*args, **kwargs)
        
        # If owner_id is provided, pre-select the owner and make the field hidden
        if owner_id:
            self.fields['owner'].initial = owner_id
            self.fields['owner'].widget = forms.HiddenInput()
            
        # Sort pet types by name
        self.fields['type'].queryset = PetType.objects.all().order_by('name')
    
    def clean_birth_date(self):
        """Validate that birth date is not in the future"""
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > date.today():
            raise ValidationError('Birth date cannot be in the future')
        return birth_date