from django.db import models
from django.urls import reverse

class Owner(models.Model):
    """Model representing a pet owner"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=80)
    telephone = models.CharField(max_length=20)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular owner instance."""
        return reverse('owners:owner-detail', args=[str(self.id)])

    def get_full_name(self):
        """Returns the owner's full name."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """String for representing the Model object."""
        return self.get_full_name()
