from django.db import models
from django.utils import timezone
from contributor.models import Contributor
from student.models import Student


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Category: {self.name}'


class Content(models.Model):
    title = models.CharField(max_length=255, default=None)
    content = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='contents')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='contents', default=None)

    def __str__(self):
        return f"Content: {self.user} - {self.description}"


class SavedContent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='saved_content')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='saved_content')