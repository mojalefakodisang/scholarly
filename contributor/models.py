from PIL import Image
from django.db import models
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager


class ContributorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CONTRIBUTOR)


class Contributor(User):

    base_role = User.Role.CONTRIBUTOR

    contributor = ContributorManager()

    class Meta:
        proxy = True


class ContributorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contributor_id = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='contr_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=Contributor)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CONTRIBUTOR":
        ContributorProfile.objects.create(user=instance)
