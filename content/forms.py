from django import forms
from .models import Content

class CreateContent(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=2)
    description = forms.CharField(max_length=500, min_length=2)
    content = forms.TextInput()

    class Meta:
        model = Content
        fields = ['title', 'description', 'content']

class UpdateContent(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=2)
    description = forms.CharField(max_length=500, min_length=2)
    content = forms.TextInput()
    
    class Meta:
        model = Content
        fields = ['title', 'description', 'content']