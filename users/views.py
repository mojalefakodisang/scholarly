import uuid
from .models import User
from django.contrib import messages
from django.contrib.auth import logout
from review.models import Review
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from content.models import Content, SavedContent
from django.core.exceptions import ValidationError
from .utils import send_email, generate_reset_token
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RequestResetForm, ResetPassword, LoginForm, UserUpdateForm
from student.models import Student, StudentProfile
from contributor.models import Contributor, ContributorProfile
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
    count = 0
    tasks = []
    notifications = []
    empty_ = ['', None]
    if request.user.first_name in empty_ or request.user.last_name in empty_:
        tasks.append('Update your profile')

    if request.user.role == 'STUDENT':
        profile = StudentProfile.objects.filter(user=request.user).first()
    elif request.user.role == 'CONTRIBUTOR':
        profile = ContributorProfile.objects.filter(user=request.user).first()

    reviews = Review.objects.all()
    review = Review.objects.filter(student=request.user).first() # fix to filter only students
    content = Content.objects.filter(user=request.user) # fix to filter only contributors
    saved = SavedContent.objects.filter(student_id=request.user.id)

    for con in content:
        for rev in reviews:
            if rev.content == con:
                count += 1
        if count == 0:
            notifications = None
        else:
            notifications.append(f'You have {count} reviews for {con.title}')



    print(request.path)

    if len(content) == 0:
        content = None
    if len(tasks) == 0:
        tasks = None

    context = {
        'title': 'Dashboard',
        'profile': profile,
        'user': request.user,
        'content': content,
        'review': review,
        'tasks': tasks,
        'notifications': notifications,
        'saved': saved
    }

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

@login_required
def update_user(request, username):
    user = User.objects.get(username=username)

    if request.user == user and user.role == 'STUDENT':
        profile = StudentProfile()
    else:
        profile = ContributorProfile()

    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'User information updated successfully')
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'users/update_user.html', context=context)