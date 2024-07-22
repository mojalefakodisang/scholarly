import uuid
from .models import User
from django.contrib import messages
from django.contrib.auth import logout
from review.models import Review
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from content.models import Content, SavedContent, ModeratedContent
from django.core.exceptions import ValidationError
from .utils import send_email, generate_reset_token, get_profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RequestResetForm, ResetPassword, LoginForm, UserUpdateForm
from student.models import StudentProfile
from moderator.models import ModeratorProfile
from contributor.models import ContributorProfile
from contributor.forms import UpdateImageForm as ContrImageForm
from student.forms import UpdateImageForm as StudImageForm
from moderator.forms import UpdateImageForm as ModImageForm
from notifications.models import Notifications
from notifications.views import create_notifications
from users.utils import get_profile
from main.utils import *


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active == True:
            login(request, user)
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
    

def statistics(request):
    l_content = obj_by_subj(Content, 'first -created_at', user=request.user)
    no_reviews = len(obj_by_subj(Review, 'all', content=l_content))
    bookmarks = len(obj_by_subj(SavedContent, 'all', content=l_content))
    r_list = [r.rating for r in obj_by_subj(Review, 'all', content=l_content)]
    avg_rating = sum(r_list) / len(r_list) if len(r_list) > 0 else 0

    return {
        'bookmarks': bookmarks,
        'no_reviews': no_reviews,
        'avg_rating': avg_rating,
        'latest_content': l_content
    }


@login_required
def dashboard(request):
    count = t_count = 0
    tasks = []
    notifications = []
    empty_ = ['', None]
    contributor_profiles = obj_all(ContributorProfile)
    if request.user.first_name in empty_ or request.user.last_name in empty_:
        tasks.append('Update your profile')

    profile = get_profile(request)
    if request.user.role == 'CONTRIBUTOR':
        create_notifications(request)

    if request.user.role == 'MODERATOR':
        moderated = obj_by_subj(
            ModeratedContent,
            'first -content',
            moderator=request.user
        )
        for c in Content.objects.all():
            if c.approved == 'Pending':
                t_count += 1
        if t_count > 0:
            tasks.append(f'You have {t_count} contents to moderate')
    else:
        moderated = None

    reviews = obj_all(Review)
    review = obj_by_subj(Review, 'first', student=request.user)
    content = Content.objects.filter(user=request.user)
    saved = obj_by_subj(
        SavedContent,
        'first -content',
        student_id=request.user.id
    )

    """Statistics"""
    l_content = statistics(request)['latest_content']
    no_reviews = statistics(request)['no_reviews']
    bookmarks = statistics(request)['bookmarks']
    avg_rating = statistics(request)['avg_rating']

    notifications = obj_by_subj(
        Notifications,
        'first -created_at',
        user=request.user
    )
    if notifications and notifications.read == False:
        not_ = notifications.title
    else:
        not_ = None

    if len(content) == 0:
        content = None
    if len(tasks) == 0:
        tasks = None

    context = {
        'bookmarks': bookmarks,
        'no_reviews': no_reviews,
        'avg_rating': avg_rating,
        'user': request.user,
        'path': request.path,
        'title': 'Dashboard',
        'profile': profile,
        'user': request.user,
        'content': content,
        'review': review,
        'tasks': tasks,
        'notifications': not_,
        'saved': saved,
        'c_profiles': contributor_profiles,
        'latest_content': l_content if l_content != None else None,
        'moderated': moderated
    }

    return render(request, 'users/dashboard.html', context=context)

def request_reset(request):
    form = RequestResetForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = obj_by_subj(User, 'first', email=email)
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
    user = obj_by_subj(User, 'first', username=username)

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
    user = obj_by_subj(User, 'first', username=username)
    profile = get_profile(request)

    if request.user.role == 'STUDENT':
        image_form = StudImageForm
    elif request.user.role == 'CONTRIBUTOR':
        image_form = ContrImageForm
    elif request.user.role == 'MODERATOR':
        image_form = ModImageForm

    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        u_form = image_form(request.POST, request.FILES, instance=profile)
        if form.is_valid() and u_form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            u_form.save()
            user.save()
            messages.success(request, 'User information updated successfully')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Failed to update user information')
    else:
        form = UserUpdateForm(instance=user)
        u_form = ContrImageForm(instance=profile)

    context = {
        'u_form': u_form,
        'form': form,
        'profile': profile
    }
    return render(request, 'users/update_user.html', context=context)

@login_required
def user_info(request, username):
    user = obj_by_subj(User, 'first', username=username)

    if not user:
        messages.warning(request, 'User not found')
        return redirect('dashboard')
    
    if user.role == 'CONTRIBUTOR':
        content = obj_by_subj(Content, 'first -created_at', user=user)
        paginator = Paginator(content, 1)
        if request.GET.get('page'):
            page_number = request.GET.get('page')
        else:
            page_number = 1
        page_obj = paginator.get_page(page_number)
        next_page = page_obj.next_page_number()\
            if page_obj.has_next() else None
        previous_page = page_obj.previous_page_number() \
            if page_obj.has_previous() else None
    else:
        page_obj = None
        page_number = 0
        next_page = None
        previous_page = None

    profile = get_profile(request)

    u_profile = get_profile(request, user=user)

    context = {
        'u_user': user,
        'u_profile': u_profile,
        'profile': profile,
        'page_obj': page_obj,
        'page_number': page_number,
        'next_page': next_page,
        'previous_page': previous_page
    }
    return render(request, 'users/user_info.html', context=context)
