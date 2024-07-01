from django.db import models
from django.utils import timezone
from student.models import Student
from content.models import Content


class Review(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    review_content = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"Review - ({self.student.username}) - Rating: {self.rating}"