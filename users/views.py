import uuid
from .models import User
from student.models import Student
from django.contrib import messages
from django.contrib.auth import logout
from review.models import Review
from content.models import Content
from contributor.models import Contributor
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ValidationError
from .utils import send_email, generate_reset_token
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RequestResetForm, ResetPassword, LoginForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'users/signin.html', context=context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')
    
@login_required
def dashboard(request):
    tasks = []
    empty_ = ['', None]
    if request.user.first_name in empty_ or request.user.last_name in empty_:
        tasks.append('Update your profile')

    review = Review.objects.filter(student=request.user).first() # fix to filter only students
    content = Content.objects.filter(user=request.user) # fix to filter only contributors
    context = {
        'title': 'Dashboard',
        'user': request.user,
        'content': content,
        'review': review,
        'tasks': tasks
    }
    print(Student.objects.filter(user=request.user).first().__dict__)
    return render(request, 'users/dashboard.html', context=context)

def request_reset(request):
    form = RequestResetForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            reset_token = generate_reset_token(user)
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
            messages.warning(request, 'Email does not exist')
            return redirect('request_reset')
        
    form = RequestResetForm()

    context = {
        'form': form
    }

    return render(request, 'users/reset_request.html', context=context)

def reset_password(request, username, token):
    user = User.objects.filter(username=username).first()

    if not user:
        messages.warning(request, 'Invalid username')
        return redirect('login')

    form = ResetPassword(request.POST)
    if form.is_valid():
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        if password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return redirect('reset_password', username=user, token=token)
        
        try:
            user.set_password(password)
            user.save()
            messages.info(request, f'{user}')
            messages.success(request, "Password reset successfully")
            return redirect('login')
        except ValidationError as e:
            messages.error(request, f"Error updating password: {e}")
            return redirect('reset_password', username=username, token=token)
    else:
        form = ResetPassword()

    context = {
        'form': form,
        'user': user
    }

    return render(request, 'users/reset_password.html', context=context)