"""Module for contributor models
"""
from PIL import Image
from django.db import models
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager


class ContributorManager(BaseUserManager):
    """Manages contributor queries

    Args:
        BaseUserManager (class): Django base user manager

    Returns:
        manager: Contributor manager
    """
    def get_queryset(self, *args, **kwargs):
        """Returns a queryset of contributors"""
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CONTRIBUTOR)


class Contributor(User):
    """Model for a Contributor user

    Args:
        User (class): User model

    Returns:
        model: Contributor user model
    """

    base_role = User.Role.CONTRIBUTOR

    contributor = ContributorManager()

    class Meta:
        proxy = True


class ContributorProfile(models.Model):
    """Model for a Contributor's profile

    Args:
        models (module): Django models module

    Returns:
        model: Contributor profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contributor_id = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='contr_pics')

    def __str__(self):
        """Returns a string representation of the ContributorProfile"""
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Saves the ContributorProfile instance"""
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Creates or updates a ContributorProfile instance"""
    if created and instance.role == User.Role.CONTRIBUTOR:
        ContributorProfile.objects.create(user=instance)
    else:
        try:
            instance.contributorprofile.save()
        except User.contributorprofile.RelatedObjectDoesNotExist:
            ContributorProfile.objects.create(user=instance)
