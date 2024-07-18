"""Module for Content models
"""
from django.db import models
from django.utils import timezone
from contributor.models import Contributor
from moderator.models import Moderator
from student.models import Student


class Category(models.Model):
    """Category model

    Attributes:
        name (str): name of the category
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        """String representation of the category"""
        return f'{self.name}'

    def save(self, *args, **kwargs):
        """Save method for the category"""
        values = self.name.split()
        super().save(*args, **kwargs)


class Content(models.Model):
    """Content model

    Attributes:
        title (str): title of the content
        content (str): content of the content
        description (str): description of the content
        created_at (datetime): date and time the content was created
        user (Contributor): contributor who created the content
        categories_str (str): categories of the content separated by commas
        categories (Category): categories of the content
        approved (str): status of the content
    """
    title = models.CharField(max_length=255, default=None)
    content = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Contributor,
                             on_delete=models.CASCADE,
                             related_name='contents')
    categories_str = models.CharField(max_length=255, default='')
    categories = models.ManyToManyField(Category, related_name='contents')
    approved = models.CharField(
        max_length=20,
        choices=[
            ('Approved', 'Approved'),
            ('Not Approved', 'Not Approved'),
            ('Pending', 'Pending')
        ],
        default='Pending'
    )

    def __str__(self):
        """String representation of the content"""
        return f"Content: {self.user} - {self.description} - {self.approved}"

    def save(self, *args, **kwargs):
        """Save method for the content"""
        super().save(*args, **kwargs)
        cat_list = [
            category.strip()
            for category in self.categories_str.split(',')
        ]

        """Add categories to the content"""
        for name in cat_list:
            category, created = Category.objects.get_or_create(name=name)
            category.save()
            self.categories.add(category)


class SavedContent(models.Model):
    """SavedContent model - Stores content saved by students

    Attributes:
        student (Student): student who saved the content
        content (Content): content saved by the student
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='saved_content'
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='saved_content'
    )


class ModeratedContent(models.Model):
    """ModeratedContent model - stores content moderated by moderators

    Attributes:
        moderator (Moderator): moderator who moderated the content
        content (Content): content moderated by the moderator
    """
    moderator = models.ForeignKey(
        Moderator,
        on_delete=models.CASCADE,
        related_name='moderated_content'
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='moderated_content'
    )
