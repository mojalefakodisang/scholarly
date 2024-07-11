from django.db import models
from users.models import User
from django.utils import timezone


class Notifications(models.Model):
    message = models.TextField()
    read = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notification: {self.user} - {self.title} - {self.read}"
