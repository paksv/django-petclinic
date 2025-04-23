from django.db import models
from django.urls import reverse
import datetime
from owners.models import Owner

class PetType(models.Model):
    """Model representing a type of pet (e.g. dog, cat, bird)"""
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Pet(models.Model):
    """Model representing a pet"""
    name = models.CharField(max_length=30)
    birth_date = models.DateField()
    type = models.ForeignKey(PetType, on_delete=models.PROTECT)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets')

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Returns the url to access a particular pet instance."""
        return reverse('pets:pet-detail', args=[str(self.id)])

    def calculate_age(self):
        """Calculate the age of the pet in years."""
        today = datetime.date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name} ({self.type})"
