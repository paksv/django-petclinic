from django.test import TestCase, Client
from django.urls import reverse
from .models import Owner
from .forms import OwnerForm
from .views import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView

class OwnerViewTests(TestCase):
    """Test cases for the Owner views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.owner1 = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            city="Anytown",
            telephone="555-1234"
        )
        self.owner2 = Owner.objects.create(
            first_name="Jane",
            last_name="Smith",
            address="456 Oak Ave",
            city="Othertown",
            telephone="555-5678"
        )
        self.list_url = reverse('owners:owner-list')
        self.detail_url = reverse('owners:owner-detail', args=[self.owner1.id])
        self.create_url = reverse('owners:owner-create')
        self.update_url = reverse('owners:owner-update', args=[self.owner1.id])
        self.search_url = reverse('owners:owner-search')

    def test_owner_list_view(self):
        """Test the owner list view"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owners/owner_list.html')
        self.assertContains(response, self.owner1.get_full_name())
        self.assertContains(response, self.owner2.get_full_name())

    def test_owner_list_view_with_search(self):
        """Test the owner list view with search"""
        response = self.client.get(f"{self.list_url}?q=John")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.owner1.get_full_name())
        self.assertNotContains(response, self.owner2.get_full_name())

    def test_owner_detail_view(self):
        """Test the owner detail view"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owners/owner_detail.html')
        self.assertContains(response, self.owner1.get_full_name())
        self.assertContains(response, self.owner1.address)
        self.assertContains(response, self.owner1.city)
        self.assertContains(response, self.owner1.telephone)

    def test_owner_create_view_get(self):
        """Test the owner create view (GET)"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owners/owner_form.html')
        self.assertIsInstance(response.context['form'], OwnerForm)

    def test_owner_create_view_post(self):
        """Test the owner create view (POST)"""
        owner_count = Owner.objects.count()
        data = {
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'address': '789 Pine St',
            'city': 'Somewhere',
            'telephone': '555-9012'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Owner.objects.count(), owner_count + 1)
        new_owner = Owner.objects.latest('id')
        self.assertEqual(new_owner.first_name, 'Bob')
        self.assertEqual(new_owner.last_name, 'Johnson')

    def test_owner_update_view_get(self):
        """Test the owner update view (GET)"""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owners/owner_form.html')
        self.assertIsInstance(response.context['form'], OwnerForm)
        self.assertEqual(response.context['form'].instance, self.owner1)

    def test_owner_update_view_post(self):
        """Test the owner update view (POST)"""
        data = {
            'first_name': 'Johnny',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'telephone': '555-1234'
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.owner1.refresh_from_db()
        self.assertEqual(self.owner1.first_name, 'Johnny')

    def test_search_owners_view(self):
        """Test the search owners view"""
        response = self.client.get(f"{self.search_url}?q=John")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owners/owner_search.html')
        self.assertContains(response, self.owner1.get_full_name())
        self.assertNotContains(response, self.owner2.get_full_name())

class OwnerFormTests(TestCase):
    """Test cases for the OwnerForm"""

    def test_valid_form(self):
        """Test that form is valid with correct data"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'telephone': '555-1234'
        }
        form = OwnerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """Test that form is invalid with blank data"""
        form = OwnerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)  # All 5 fields are required

    def test_telephone_validation(self):
        """Test telephone validation"""
        # Valid telephone formats
        valid_telephones = ['555-1234', '(555) 123-4567', '5551234', '555 123 4567']
        for telephone in valid_telephones:
            data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'address': '123 Main St',
                'city': 'Anytown',
                'telephone': telephone
            }
            form = OwnerForm(data=data)
            self.assertTrue(form.is_valid(), f"Form should be valid with telephone: {telephone}")

        # Invalid telephone formats
        invalid_telephones = ['555-ABCD', '555.1234', '555@1234']
        for telephone in invalid_telephones:
            data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'address': '123 Main St',
                'city': 'Anytown',
                'telephone': telephone
            }
            form = OwnerForm(data=data)
            self.assertFalse(form.is_valid(), f"Form should be invalid with telephone: {telephone}")
            self.assertIn('telephone', form.errors)

class OwnerModelTests(TestCase):
    """Test cases for the Owner model"""

    def setUp(self):
        """Set up test data"""
        self.owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            city="Anytown",
            telephone="555-1234"
        )

    def test_owner_creation(self):
        """Test that an owner can be created"""
        self.assertEqual(self.owner.first_name, "John")
        self.assertEqual(self.owner.last_name, "Doe")
        self.assertEqual(self.owner.address, "123 Main St")
        self.assertEqual(self.owner.city, "Anytown")
        self.assertEqual(self.owner.telephone, "555-1234")

    def test_get_full_name(self):
        """Test the get_full_name method"""
        self.assertEqual(self.owner.get_full_name(), "John Doe")

    def test_string_representation(self):
        """Test the string representation of an owner"""
        self.assertEqual(str(self.owner), "John Doe")

    def test_get_absolute_url(self):
        """Test the get_absolute_url method"""
        url = self.owner.get_absolute_url()
        expected_url = reverse('owners:owner-detail', args=[str(self.owner.id)])
        self.assertEqual(url, expected_url)
