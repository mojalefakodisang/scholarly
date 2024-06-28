from django.test import TestCase
from .models import Contributor


class ContributorModelTest(TestCase):
    def test_create_user(self):
        """Test creating a new user"""
        username = 'test'
        email = 'test@example.com'
        password = 'testpass123'
        user = Contributor.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.role, "CONTRIBUTOR")
        self.assertTrue(user.check_password(password))