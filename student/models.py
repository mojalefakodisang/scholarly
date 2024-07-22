from PIL import Image
from django.db import models
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        """
        Returns a queryset containing only the students.

        This method filters the queryset returned by the
        parent class to include only the students.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            QuerySet: A queryset containing only the students.
        """
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):
    """
    Represents a student user.

    Inherits from the User class and adds additional functionality
    specific to students.
    """

    base_role = User.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy = True


class StudentProfile(models.Model):
    """
    Represents a student profile.

    Attributes:
        user (User): The user associated with the student profile.
        student_id (int): The student's ID.
        image (ImageField): The profile image of the student.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='stud_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile based on the user's role.

    Args:
        sender: The model class that sent the signal.
        instance: The actual instance being saved.
        created: A boolean value indicating whether the instance was
            created or not.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created and instance.role == User.Role.STUDENT:
        StudentProfile.objects.create(user=instance)
    else:
        try:
            instance.studentprofile.save()
        except User.studentprofile.RelatedObjectDoesNotExist:
            StudentProfile.objects.create(user=instance)