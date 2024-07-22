from django.db import models
from django.utils import timezone
from student.models import Student
from content.models import Content


class Review(models.Model):
    RATING_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='review')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    review_content = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Returns a string representation of the Review object.

        The string includes the username of the student who wrote the review
        and the rating given for the review.

        Returns:
            str: A string representation of the Review object.
        """
        return f"Review - ({self.student.username}) - Rating: {self.rating}"

    def __doc__(self):
        """
        Returns the docstring for the Review class.

        Returns:
            str: The docstring for the Review class.
        """
        return """
        The Review class represents a review given by a student for a content.

        Attributes:
            content (ForeignKey): The content for which the review is given.
            student (ForeignKey): The student who wrote the review.
            rating (IntegerField): The rating given for the review.
            review_content (CharField): The content of the review.
            created_at (DateTimeField): The timestamp when the review was created.
        """
