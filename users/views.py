import uuid
from .models import User
from django.contrib import messages
from django.contrib.auth import logout
from review.models import Review
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from content.models import Content, SavedContent, ModeratedContent
from django.core.exceptions import ValidationError
from .utils import send_email, generate_reset_token
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RequestResetForm, ResetPassword, LoginForm, UserUpdateForm
from student.models import StudentProfile
from moderator.models import ModeratorProfile
from contributor.models import ContributorProfile
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
        'title': 'Scholarly | Login',
        'form': form
    }
    return render(request, 'users/signin.html', context=context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')
    
@login_required
def dashboard(request):
    n_count = t_count = 0
    tasks = []
    notifications = []
    empty_ = ['', None]
    moderated = []
    if request.user.first_name in empty_ or request.user.last_name in empty_:
        tasks.append('Update your profile')
    
    reviews = Review.objects.all()
    review = Review.objects.filter(student=request.user).first()
    content = Content.objects.filter(user=request.user).order_by('-created_at')
    contents = Content.objects.all() # All contents
    saved = SavedContent.objects.filter(student_id=request.user.id).first()

    for cont in contents:
        if cont.approved != 'Approved':
            t_count += 1

    if request.user.role == 'STUDENT':
        profile = StudentProfile.objects.filter(user=request.user).first()

    elif request.user.role == 'CONTRIBUTOR':
        profile = ContributorProfile.objects.filter(user=request.user).first()
        
    elif request.user.role == 'MODERATOR':
        profile = ModeratorProfile.objects.filter(user=request.user).first()
        if t_count > 0:
            tasks.append(f'You have {t_count} contents to moderate')
        moderated = ModeratedContent.objects.filter(moderator=request.user).all()

    for con in content:
        for rev in reviews:
            if rev.content == con:
                n_count += 1
        if n_count == 0:
            notifications = None
        else:
            notifications.append(f'You have {n_count} reviews for {con.title}')

    if len(content) == 0:
        content = None
    if len(tasks) == 0:
        tasks = None

    context = {
        'title': 'Dashboard',
        'path': request.path,
        'profile': profile,
        'user': request.user,
        'content': content,
        'review': review,
        'tasks': tasks,
        'notifications': notifications,
        'saved': saved,
        'bookmarks': 1,
        'ratings': 0,
        'reviews': 0,
        'moderated': moderated,
        'latest_content': content[0] if content != None else None
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
            https://scholarlyonline.live/reset_password/{user.username}/{reset_token}\n\n
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
    elif request.user == user and user.role == 'CONTRIBUTOR':
        profile = ContributorProfile()
    elif request.user == user and user.role == 'MODERATOR':
        profile = ModeratorProfile()

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