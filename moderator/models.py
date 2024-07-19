"""Module for Moderator models
"""
from PIL import Image
from django.db import models
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager


class ModeratorManager(BaseUserManager):
    """Manages Moderator queries

    Args:
        BaseUserManager (class): Django base user manager

    Returns:
        manager: Moderator manager
    """
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MODERATOR)


class Moderator(User):
    """Model for a Moderator user

    Args:
        User (class): User model

    Returns:
        model: Moderator user model
    """
    base_role = User.Role.MODERATOR

    moderator = ModeratorManager()

    class Meta:
        proxy = True


class ModeratorProfile(models.Model):
    """Model for a Moderator's profile

    Args:
        models (module): Django models module

    Returns:
        model: Moderator profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    moderator_id = models.IntegerField(null=True, blank=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='moderator_pics')

    def __str__(self):
        """Returns a string representation of the ModeratorProfile"""
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Saves the ModeratorProfile instance"""
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Creates or updates a ModeratorProfile instance"""
    if created and instance.role == User.Role.CONTRIBUTOR:
        ModeratorProfile.objects.create(user=instance)
    else:
        try:
            instance.moderatorprofile.save()
        except User.moderatorprofile.RelatedObjectDoesNotExist:
            ModeratorProfile.objects.create(user=instance)
