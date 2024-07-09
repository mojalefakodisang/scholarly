from django import forms
from .models import Moderator, ModeratorProfile
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Moderator
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['email'].help_text = ""
        self.fields['password1'].help_text = ""

class UpdateImageForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = ModeratorProfile
        fields = ['image']