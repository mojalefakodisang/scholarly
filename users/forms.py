from django import forms
from .models import User


class RequestResetForm(forms.Form):
    email = forms.EmailField()


class ResetPassword(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']