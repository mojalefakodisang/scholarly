from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .models import Student
from users.models import User
from users.utils import get_profile
from main.utils import *


def register(request):
    """
    View function for registering a student.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        None
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already taken')
                return redirect('st-register')
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username is already taken')
                return redirect('st-register')
            if password1 != password2:
                messages.warning(
                    request, 
                    'Passwords does not match, please try again'
                )
                return redirect('st-register')

            Student.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(
                request, 
                'Student registered successfully. You can now login'
            )
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'title': 'Scholarly | Student - Register',
        'form': form
    }
    return render(request, 'student/register.html', context=context)
