"""Tests for content models"""
from django.test import TestCase
from .models import Content, Category
from contributor.models import Contributor

class Model1TestCase(TestCase):
    def setUp(self):
        contr1 = Contributor(
            username='test',
            email='test@gmail.com',
            password='testing321'
        )
        contr1.save()

    def test_create_content(self):
        title = 'This is the test title'
        description = 'This is the test description'
        category = 'Other'
        content = 'This is the test content'
        
        content1 = Content(
            title=title,
            description=description,
            categories_str=category,
            content=content,
            user=Contributor.objects.get(username='test')
        )
        content1.save()

        self.assertEqual(content1.title, title)
        self.assertEqual(content1.description, description)
        self.assertEqual(content1.categories_str, category)
        self.assertEqual(content1.content, content)
        self.assertEqual(content1.user.username, 'test')
        self.assertEqual(content1.approved, 'Pending')
        