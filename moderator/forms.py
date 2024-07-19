"""Forms module for Moderators
"""
from django import forms
from .models import Moderator, ModeratorProfile
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """Register form for a Moderator user

    Args:
        UserCreationForm (class): Form for creating a new user

    Returns:
        form: Form for creating a new Moderator user
    """
    email = forms.EmailField()

    class Meta:
        model = Moderator
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """Initializes RegisterForm instance"""
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['email'].help_text = ""
        self.fields['password1'].help_text = ""

class UpdateImageForm(forms.ModelForm):
    """Form for updating a Moderator's profile image

    Args:
        forms (module): Django forms module

    Returns:
        form: Form for updating a Moderator's profile image
    """
    image = forms.ImageField()
    class Meta:
        model = ModeratorProfile
        fields = ['image']