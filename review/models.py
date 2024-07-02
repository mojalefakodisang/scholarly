from django.db import models
from django.utils import timezone
from student.models import Student
from content.models import Content


class Review(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='review')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(default=0)
    review_content = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review - ({self.student.username}) - Rating: {self.rating}"