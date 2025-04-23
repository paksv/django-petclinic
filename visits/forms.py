from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from .models import Visit
from pets.models import Pet

class VisitForm(forms.ModelForm):
    """Form for creating and updating Visit instances"""
    
    class Meta:
        model = Visit
        fields = ['date', 'description', 'pet']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pet': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        pet_id = kwargs.pop('pet_id', None)
        super(VisitForm, self).__init__(*args, **kwargs)
        
        # If pet_id is provided, pre-select the pet and make the field hidden
        if pet_id:
            self.fields['pet'].initial = pet_id
            self.fields['pet'].widget = forms.HiddenInput()
            
        # Set default date to today if creating a new visit
        if not self.instance.pk and not self.initial.get('date'):
            self.initial['date'] = date.today()
    
    def clean_date(self):
        """Validate that visit date is not in the future"""
        visit_date = self.cleaned_data.get('date')
        if visit_date and visit_date > date.today():
            raise ValidationError('Visit date cannot be in the future')
        return visit_date