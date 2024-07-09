from django import forms
from .models import Student, StudentProfile
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            "password2": "Confirm Password",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['email'].help_text = ""
        self.fields['password1'].help_text = ""

class UpdateImageForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = StudentProfile
        fields = ['image']