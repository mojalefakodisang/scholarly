from django.test import TestCase
from .models import Student


class StudentModelTest(TestCase):
    def test_create_user(self):
        """Test creating a new user"""
        username = 'test'
        email = 'test@example.com'
        password = 'testpass123'
        user = Student.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.role, "STUDENT")
        self.assertTrue(user.check_password(password))