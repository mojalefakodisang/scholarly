from django.db import models
from django.utils import timezone
from contributor.models import Contributor


class Content(models.Model):
    content = models.TextField()
    # category = models.ManyToOneRel()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())
    user = models.OneToOneField(Contributor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.description}"
