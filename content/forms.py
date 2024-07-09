from django import forms
from .models import Content, Category

class CreateContent(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=2)
    description = forms.CharField(max_length=500, min_length=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    content = forms.TextInput()

    class Meta:
        model = Content
        fields = ['title', 'category', 'description', 'content']

class UpdateContent(forms.ModelForm):
    title = forms.CharField(max_length=255, min_length=2)
    description = forms.CharField(max_length=500, min_length=2)
    content = forms.TextInput()
    
    class Meta:
        model = Content
        fields = ['title', 'category', 'description', 'content']

class CreateCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=255, min_length=2)

    class Meta:
        model = Category
        fields = ['name']