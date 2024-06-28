from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Student


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            Student.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'title': 'Student - Register',
        'form': form
    }
    return render(request, 'student/register.html', context=context)