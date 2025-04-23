from django.db import models
from django.urls import reverse

class Specialty(models.Model):
    """Model representing a veterinary specialty (e.g. dentistry, surgery)"""
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'specialties'

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Vet(models.Model):
    """Model representing a veterinarian"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    specialties = models.ManyToManyField(Specialty, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular vet instance."""
        return reverse('vets:vet-detail', args=[str(self.id)])

    def get_full_name(self):
        """Returns the vet's full name."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """String for representing the Model object."""
        return self.get_full_name()
