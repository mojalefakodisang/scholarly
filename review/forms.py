from django import forms
from .models import Review


class CreateReview(forms.ModelForm):
    review_content = forms.CharField(max_length=255)
    rating = forms.NumberInput()

    class Meta:
        model = Review
        fields = ['review_content', 'rating']


class UpdateReview(forms.ModelForm):
    review_content = forms.CharField(max_length=255)
    rating = forms.NumberInput()

    class Meta:
        model = Review
        fields = ['review_content', 'rating']