from django.db import models
from django.utils import timezone
from contributor.models import Contributor
from moderator.models import Moderator
from student.models import Student


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        values = self.name.split()
        super().save(*args, **kwargs)


class Content(models.Model):
    title = models.CharField(max_length=255, default=None)
    content = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='contents')
    categories_str = models.CharField(max_length=255, default='')
    categories = models.ManyToManyField(Category, related_name='contents')
    approved = models.CharField(max_length=20, choices=[('Approved', 'Approved'),
                                                        ('Not Approved', 'Not Approved'),
                                                        ('Pending', 'Pending')],
                                                        default='Pending')

    def __str__(self):
        return f"Content: {self.user} - {self.description} - {self.approved}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cat_list = [category.strip() for category in self.categories_str.split(',')]

        for name in cat_list:
            category, created = Category.objects.get_or_create(name=name)
            category.save()
            self.categories.add(category)




class SavedContent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='saved_content')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='saved_content')


class ModeratedContent(models.Model):
    moderator = models.ForeignKey(Moderator, on_delete=models.CASCADE, related_name='moderated_content')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='moderated_content')