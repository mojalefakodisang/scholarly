from django import forms
from .models import Review


class CreateReview(forms.ModelForm):
    review_content = forms.CharField(max_length=255)
    rating = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['review_content', 'rating']


class UpdateReview(forms.ModelForm):
    review_content = forms.CharField(max_length=255)
    rating = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['review_content', 'rating']