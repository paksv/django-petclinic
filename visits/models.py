from django.db import models
from django.urls import reverse
from pets.models import Pet

class Visit(models.Model):
    """Model representing a visit to the veterinarian"""
    date = models.DateField()
    description = models.TextField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='visits')

    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        """Returns the url to access a particular visit instance."""
        return reverse('visits:visit-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.pet} - {self.date}"
