from django.db import models
from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        CONTRIBUTOR = "CONTRIBUTOR", "Contributor"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)

    @property
    def studentprofile(self):
        StudentProfile = apps.get_model('student', 'StudentProfile')
        return StudentProfile.objects.get(user=self)

    @property
    def contributorprofile(self):
        ContributorProfile = apps.get_model('contributor', 'ContributorProfile')
        return ContributorProfile.objects.get(user=self)