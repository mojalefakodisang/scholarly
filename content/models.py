from django.db import models
from django.utils import timezone
from contributor.models import Contributor


class Content(models.Model):
    title = models.CharField(max_length=255, default=None)
    content = models.TextField()
    # category = models.ManyToOneRel()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='contents')

    def __str__(self):
        return f"{self.user} - {self.description}"
