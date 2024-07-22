from django.db import models
from users.models import User
from django.utils import timezone


class Notifications(models.Model):
    """
    Represents a notification for a user.

    Attributes:
        message (str): The content of the notification.
        read (bool): Indicates whether the notification has been read or not.
        title (str): The title of the notification.
        created_at (datetime): The timestamp when the notification was created.
        user (User): The user associated with the notification.
    """

    message = models.TextField()
    read = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f"Notification: {self.user} - {self.title} - {self.read}"
