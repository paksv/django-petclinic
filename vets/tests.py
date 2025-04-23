from django.test import TestCase
from django.urls import reverse
from .models import Vet, Specialty
from .forms import VetForm

class VetFormTests(TestCase):
    """Test cases for the VetForm"""

    def setUp(self):
        """Set up test data"""
        self.specialty1 = Specialty.objects.create(name="Surgery")
        self.specialty2 = Specialty.objects.create(name="Dentistry")

    def test_valid_form(self):
        """Test that form is valid with correct data"""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'specialties': [self.specialty1.id, self.specialty2.id]
        }
        form = VetForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """Test that form is invalid with blank data"""
        form = VetForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # first_name and last_name are required

    def test_specialties_optional(self):
        """Test that specialties field is optional"""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'specialties': []
        }
        form = VetForm(data=data)
        self.assertTrue(form.is_valid())

    def test_specialties_ordering(self):
        """Test that specialties are ordered by name"""
        form = VetForm()
        # Get the first two specialties from the queryset
        specialties = list(form.fields['specialties'].queryset[:2])
        # Check that they are in alphabetical order
        self.assertEqual(specialties[0].name, "Dentistry")
        self.assertEqual(specialties[1].name, "Surgery")

    def test_help_text(self):
        """Test that help text is set for specialties field"""
        form = VetForm()
        self.assertIn("Hold down Ctrl", form.fields['specialties'].help_text)

class SpecialtyModelTests(TestCase):
    """Test cases for the Specialty model"""

    def setUp(self):
        """Set up test data"""
        self.specialty = Specialty.objects.create(name="Surgery")

    def test_specialty_creation(self):
        """Test that a specialty can be created"""
        self.assertEqual(self.specialty.name, "Surgery")

    def test_string_representation(self):
        """Test the string representation of a specialty"""
        self.assertEqual(str(self.specialty), "Surgery")

    def test_verbose_name_plural(self):
        """Test the verbose_name_plural of the Specialty model"""
        self.assertEqual(Specialty._meta.verbose_name_plural, "specialties")

class VetModelTests(TestCase):
    """Test cases for the Vet model"""

    def setUp(self):
        """Set up test data"""
        self.specialty1 = Specialty.objects.create(name="Surgery")
        self.specialty2 = Specialty.objects.create(name="Dentistry")
        self.vet = Vet.objects.create(
            first_name="Jane",
            last_name="Smith"
        )
        self.vet.specialties.add(self.specialty1, self.specialty2)

    def test_vet_creation(self):
        """Test that a vet can be created"""
        self.assertEqual(self.vet.first_name, "Jane")
        self.assertEqual(self.vet.last_name, "Smith")
        self.assertEqual(self.vet.specialties.count(), 2)
        self.assertIn(self.specialty1, self.vet.specialties.all())
        self.assertIn(self.specialty2, self.vet.specialties.all())

    def test_get_full_name(self):
        """Test the get_full_name method"""
        self.assertEqual(self.vet.get_full_name(), "Jane Smith")

    def test_string_representation(self):
        """Test the string representation of a vet"""
        self.assertEqual(str(self.vet), "Jane Smith")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        url = self.vet.get_absolute_url()
        expected_url = reverse('vets:vet-detail', args=[str(self.vet.id)])
        self.assertEqual(url, expected_url)
