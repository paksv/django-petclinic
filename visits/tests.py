from django.test import TestCase
from django.urls import reverse
import datetime
from django.forms import HiddenInput
from .models import Visit
from .forms import VisitForm
from pets.models import Pet, PetType
from owners.models import Owner

class VisitFormTests(TestCase):
    """Test cases for the VisitForm"""

    def setUp(self):
        """Set up test data"""
        self.owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            city="Anytown",
            telephone="555-1234"
        )
        self.pet_type = PetType.objects.create(name="Dog")
        self.pet = Pet.objects.create(
            name="Fido",
            birth_date=datetime.date(2018, 1, 1),
            type=self.pet_type,
            owner=self.owner
        )

    def test_valid_form(self):
        """Test that form is valid with correct data"""
        data = {
            'date': datetime.date.today(),
            'description': 'Annual checkup',
            'pet': self.pet.id
        }
        form = VisitForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """Test that form is invalid with blank data"""
        form = VisitForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # All 3 fields are required

    def test_future_date(self):
        """Test validation for future date"""
        # Get a future date
        future_date = datetime.date.today() + datetime.timedelta(days=30)

        data = {
            'date': future_date,
            'description': 'Annual checkup',
            'pet': self.pet.id
        }
        form = VisitForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_pet_id_parameter(self):
        """Test that pet_id parameter works correctly"""
        # Create form with pet_id parameter
        form = VisitForm(pet_id=self.pet.id)

        # Check that pet field is hidden and pre-selected
        self.assertIsInstance(form.fields['pet'].widget, HiddenInput)
        self.assertEqual(form.fields['pet'].initial, self.pet.id)

    def test_default_date(self):
        """Test that default date is set to today for new visits"""
        form = VisitForm()
        self.assertEqual(form.initial['date'], datetime.date.today())

class VisitModelTests(TestCase):
    """Test cases for the Visit model"""

    def setUp(self):
        """Set up test data"""
        self.owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            city="Anytown",
            telephone="555-1234"
        )
        self.pet_type = PetType.objects.create(name="Dog")
        self.pet = Pet.objects.create(
            name="Fido",
            birth_date=datetime.date(2018, 1, 1),
            type=self.pet_type,
            owner=self.owner
        )
        self.visit = Visit.objects.create(
            date=datetime.date(2023, 1, 15),
            description="Annual checkup",
            pet=self.pet
        )

    def test_visit_creation(self):
        """Test that a visit can be created"""
        self.assertEqual(self.visit.date, datetime.date(2023, 1, 15))
        self.assertEqual(self.visit.description, "Annual checkup")
        self.assertEqual(self.visit.pet, self.pet)

    def test_string_representation(self):
        """Test the string representation of a visit"""
        expected_str = f"{self.pet} - {self.visit.date}"
        self.assertEqual(str(self.visit), expected_str)

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        url = self.visit.get_absolute_url()
        expected_url = reverse('visits:visit-detail', args=[str(self.visit.id)])
        self.assertEqual(url, expected_url)

    def test_ordering(self):
        """Test that visits are ordered by date in descending order"""
        # Create another visit with a different date
        visit2 = Visit.objects.create(
            date=datetime.date(2023, 2, 15),
            description="Follow-up",
            pet=self.pet
        )

        # Get all visits for the pet
        visits = Visit.objects.filter(pet=self.pet)

        # Check that the newer visit comes first
        self.assertEqual(visits[0], visit2)
        self.assertEqual(visits[1], self.visit)
