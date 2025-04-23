from django import forms
from .models import Owner

class OwnerForm(forms.ModelForm):
    """Form for creating and updating Owner instances"""
    
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'address', 'city', 'telephone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 123-456-7890'}),
        }
        
    def clean_telephone(self):
        """Validate telephone number format"""
        telephone = self.cleaned_data.get('telephone')
        # Simple validation - ensure it contains only digits, spaces, dashes, and parentheses
        if telephone and not all(char.isdigit() or char in ' -()' for char in telephone):
            raise forms.ValidationError('Telephone number should contain only digits, spaces, dashes, and parentheses.')
        return telephone