from django.db import models
from django.utils import timezone
from contributor.models import Contributor
from moderator.models import Moderator
from student.models import Student


class Category(models.Model):
    name = models.CharField(max_length=100, default='Other')

    def __str__(self):
        return f'Category: {self.name}'


class Content(models.Model):
    title = models.CharField(max_length=255, default=None)
    content = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='contents')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='contents', default=None)
    approved = models.CharField(max_length=20, choices=[('Approved', 'Approved'),
                                                        ('Not Approved', 'Not Approved'),
                                                        ('Pending', 'Pending')],
                                                        default='Pending')

    def __str__(self):
        return f"Content: {self.user} - {self.description} - {self.status}"


class SavedContent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='saved_content')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='saved_content')


class ModeratedContent(models.Model):
    moderator = models.ForeignKey(Moderator, on_delete=models.CASCADE, related_name='moderated_content')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='moderated_content')