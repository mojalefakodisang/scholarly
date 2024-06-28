import uuid
from .models import User
from .utils import send_email
from student.models import Student
from django.contrib import messages
from django.contrib.auth import logout
from contributor.models import Contributor
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from .forms import RequestResetForm, ResetPassword
from django.contrib.auth.decorators import login_required

reset_token = ''

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')
    
@login_required
def dashboard(request):
    role = request.user.role
    context = {
        'role': role,
        'user': request.user
    }
    return render(request, 'users/dashboard.html', context=context)

def request_reset(request):
    form = RequestResetForm(request.POST)
    if form.is_valid():
        reset_token = uuid.uuid4()
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            subject = "Request to reset password | Scholarly"
            receiver = email
            body = f"""\
            Hi {user.username},\n\n
            You have requested to reset your password.\n
            To proceed, please click the link below:\n
            http://localhost:8000/reset_password/{user.username}/{reset_token}\n\n
            Regards,\n
            Technical Team, Scholarly
            """
            send_email(receiver, subject, body)
            messages.success(request, 'Request sent. Please check your email')
            return redirect('login')
        else:
            messages.error(request, 'Email does not exist')
            return redirect('request_reset')
    form = RequestResetForm()

    context = {
        'form': form
    }

    return render(request, 'users/reset_request.html', context=context)

def reset_password(request, username, token):
    form = ResetPassword(request.POST)
    user = User.objects.filter(username=username).first()
    if form.is_valid() and token == reset_token and user is not None:
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        messages.success(request, "Password reset successfully")
        return redirect('login')
    else:
        form = ResetPassword()

    context = {
        'form': form,
        'user': user
    }

    return render(request, 'users/reset_password.html', context=context)