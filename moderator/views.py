"""Views for the moderator app
"""
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Moderator, ModeratorProfile
from users.utils import send_email
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from users.models import User as u_User
from content.models import Content, ModeratedContent
from django.contrib.auth.decorators import login_required


def register(request):
    """View for registering a new Moderator user

    Args:
        request (HttpRequest): HttpRequest object

    Returns:
        HttpResponse: HttpResponse object
    """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if u_User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already taken')
                return redirect('mod-register')
            if u_User.objects.filter(username=username).exists():
                messages.warning(request, 'Username is already taken')
                return redirect('mod-register')
            if password1 != password2:
                messages.warning(
                    request,
                    'Passwords does not match, please try again'
                )
                return redirect('mod-register')

            user = Moderator.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)

            profile = ModeratorProfile(user=user, token=token)
            profile.save()
            link = f'https://scholarlyonline.live/validate/?token={token}'
            subject = 'Account Validation'
            message = '{}{}'.format(
                'Please click the link below to validate your account:\n\n',
                link
            )

            send_email(dest=email, subject=subject, body=message)
            messages.success(
                request,
                'Email sent to validate your account.\
                    Please check your email to continue'
            )
            return redirect('login')
        else:
            messages.warning(request, 'Registration failed. Please try again')
    else:
        form = RegisterForm()

    context = {
        'title': 'moderator - Register',
        'form': form
    }
    return render(request, 'moderator/register.html', context=context)


def validate(request):
    """View for validating a Moderator user account"""
    token = request.GET.get('token')
    try:
        profile = ModeratorProfile.objects.get(token=token)
        user = profile.user
        user.is_active = True
        user.save()
        messages.success(
            request,
            'Account validated successfully. You can now login.'
        )
    except User.DoesNotExist:
        messages.error(request, 'Invalid token. Please try again.')
    return redirect('login')


@login_required
def approve_content(request, content_id):
    """View for approving content

    Args:
        request (HttpRequest): HttpRequest object
        content_id (int): Content ID

    Returns:
        HttpResponse: HttpResponse object
    """
    content = Content.objects.get(id=content_id)

    if content is None:
        messages.warning(request, 'Content not found. Please try again')
        return redirect('explore')

    if content.approved == 'Approved':
        messages.success(request, 'Content already approved')
        return redirect('explore')

    content.approved = 'Approved'
    content.save()
    mod = ModeratedContent(moderator=request.user, content=content)
    mod.save()
    messages.success(request, 'Content approved successfully')
    return redirect('explore')


@login_required
def disapprove_content(request, content_id):
    """View for disapproving content

    Args:
        request (HttpRequest): HttpRequest object
        content_id (int): Content ID

    Returns:
        HttpResponse: HttpResponse object
    """
    content = Content.objects.get(id=content_id)
    mod = ModeratedContent.objects.filter(content=content).all()

    if content is None:
        messages.warning(request, 'Content not found. Please try again')
        return redirect('explore')

    content.approved = 'Not Approved'
    content.save()
    mod.delete()
    messages.success(request, 'Content disapproved successfully')
    return redirect('explore')
