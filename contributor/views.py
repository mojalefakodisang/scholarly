from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Contributor


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            Contributor.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'title': 'Contributor - Register',
        'form': form
    }
    return render(request, 'contributor/register.html', context=context)