from django import forms
from .models import Content, Category

class CreateContent(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=2)
    description = forms.CharField(max_length=500, min_length=2)
    categories_str = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter categories separated by commas'}))
    content = forms.TextInput()

    class Meta:
        model = Content
        fields = ['title', 'categories_str', 'description', 'content']

class UpdateContent(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=2)
    description = forms.CharField(max_length=500, min_length=2)
    categories_str = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter categories separated by commas'}))
    content = forms.TextInput()
    
    class Meta:
        model = Content
        fields = ['title', 'description', 'categories_str', 'content']