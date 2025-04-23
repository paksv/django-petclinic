from django.test import TestCase
from django.urls import reverse
import datetime
from django.forms import HiddenInput
from .models import Pet, PetType
from .forms import PetForm
from owners.models import Owner

class PetFormTests(TestCase):
    """Test cases for the PetForm"""

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

    def test_valid_form(self):
        """Test that form is valid with correct data"""
        data = {
            'name': 'Fido',
            'birth_date': '2018-01-01',
            'type': self.pet_type.id,
            'owner': self.owner.id
        }
        form = PetForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """Test that form is invalid with blank data"""
        form = PetForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # All 4 fields are required

    def test_future_birth_date(self):
        """Test validation for future birth date"""
        # Get a future date
        future_date = datetime.date.today() + datetime.timedelta(days=30)

        data = {
            'name': 'Fido',
            'birth_date': future_date,
            'type': self.pet_type.id,
            'owner': self.owner.id
        }
        form = PetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)

    def test_owner_id_parameter(self):
        """Test that owner_id parameter works correctly"""
        # Create form with owner_id parameter
        form = PetForm(owner_id=self.owner.id)

        # Check that owner field is hidden and pre-selected
        self.assertIsInstance(form.fields['owner'].widget, HiddenInput)
        self.assertEqual(form.fields['owner'].initial, self.owner.id)

class PetTypeModelTests(TestCase):
    """Test cases for the PetType model"""

    def setUp(self):
        """Set up test data"""
        self.pet_type = PetType.objects.create(name="Dog")

    def test_pet_type_creation(self):
        """Test that a pet type can be created"""
        self.assertEqual(self.pet_type.name, "Dog")

    def test_string_representation(self):
        """Test the string representation of a pet type"""
        self.assertEqual(str(self.pet_type), "Dog")

class PetModelTests(TestCase):
    """Test cases for the Pet model"""

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

    def test_pet_creation(self):
        """Test that a pet can be created"""
        self.assertEqual(self.pet.name, "Fido")
        self.assertEqual(self.pet.birth_date, datetime.date(2018, 1, 1))
        self.assertEqual(self.pet.type, self.pet_type)
        self.assertEqual(self.pet.owner, self.owner)

    def test_calculate_age(self):
        """Test the calculate_age method"""
        # Calculate expected age based on birth date and current date
        today = datetime.date.today()
        expected_age = today.year - 2018 - ((today.month, today.day) < (1, 1))
        self.assertEqual(self.pet.calculate_age(), expected_age)

    def test_string_representation(self):
        """Test the string representation of a pet"""
        self.assertEqual(str(self.pet), "Fido (Dog)")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        url = self.pet.get_absolute_url()
        expected_url = reverse('pets:pet-detail', args=[str(self.pet.id)])
        self.assertEqual(url, expected_url)
