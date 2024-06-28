from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        """Test creating a new user"""
        username = 'test'
        email = 'test@example.com'
        password = 'testpass123'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.role, "ADMIN")
        self.assertTrue(user.check_password(password))