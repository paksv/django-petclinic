from django import forms
from .models import Vet, Specialty

class VetForm(forms.ModelForm):
    """Form for creating and updating Vet instances"""
    
    class Meta:
        model = Vet
        fields = ['first_name', 'last_name', 'specialties']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialties': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(VetForm, self).__init__(*args, **kwargs)
        
        # Sort specialties by name
        self.fields['specialties'].queryset = Specialty.objects.all().order_by('name')
        self.fields['specialties'].help_text = "Hold down Ctrl (or Command on Mac) to select multiple specialties"