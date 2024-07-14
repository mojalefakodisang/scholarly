from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Contributor
from django.contrib import messages
from users.models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already taken')
                return redirect('contr-register')
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username is already taken')
                return redirect('contr-register')
            if password1 != password2:
                messages.warning(request, 'Passwords does not match, please try again')
                return redirect('contr-register')
            
            Contributor.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(request, 'Student registered successfully. You can now login')
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'title': 'Scholarly | Student - Register',
        'form': form
    }
    return render(request, 'contributor/register.html', context=context)