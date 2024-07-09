from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Moderator, ModeratorProfile
from users.utils import send_email
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from content.models import Content, ModeratedContent
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            
            user = Moderator.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            
            profile = ModeratorProfile(user=user, token=token)
            profile.save()
            subject = 'Account Validation'
            message = f'Please click the link below to validate your account:\n\n{request.build_absolute_uri("/validate/")}?token={token}'

            send_email(dest=email, subject=subject, body=message)
            messages.success(request, 'Email sent to validate your account. Please check your email to continue')
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
    token = request.GET.get('token')
    try:
        profile = ModeratorProfile.objects.get(token=token)
        user = profile.user
        user.is_active = True   
        user.save()
        messages.success(request, 'Account validated successfully. You can now login.')
    except User.DoesNotExist:
        messages.error(request, 'Invalid token. Please try again.')
    return redirect('login')

@login_required
def approve_content(request, content_id):
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
    content = Content.objects.get(id=content_id)
    mod = ModeratedContent.objects.get(content=content)

    if content is None:
        messages.warning(request, 'Content not found. Please try again')
        return redirect('explore')

    content.approved = 'Not Approved'
    content.save()
    mod.delete()
    messages.success(request, 'Content disapproved successfully')
    return redirect('explore')