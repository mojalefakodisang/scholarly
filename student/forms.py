from django import forms
from .models import Student, StudentProfile
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """
    A form for registering a new student.

    Inherits from UserCreationForm and adds an email field.

    Attributes:
        email (forms.EmailField): The email field for the student.

    Meta:
        model (Student): The model associated with the form.
        fields (list): The fields to include in the form.
        labels (dict): The labels for specific fields in the form.

    Methods:
        __init__: Initializes the form and sets the help text for
            specific fields.
    """
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
        """
        The `Meta` class provides metadata options for the `StudentProfile`
            form.

        Attributes:
            model (Model): The model class that the form is based on.
            fields (list): The list of fields to include in the form.
        """
        model = StudentProfile
        fields = ['image']