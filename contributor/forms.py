from django import forms
from .models import Contributor
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Contributor
        fields = ['username', 'email', 'password1', 'password2']

