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


@receiver(post_save, sender=Contributor)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CONTRIBUTOR":
        ContributorProfile.objects.create(user=instance)
