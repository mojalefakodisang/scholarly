from .models import Content
from review.models import Review
from django.contrib import messages
from student.models import StudentProfile
from django.shortcuts import render, redirect
from .forms import CreateContent, UpdateContent
from django.contrib.auth.decorators import login_required
from contributor.models import Contributor, ContributorProfile


@login_required
def create_content(request):
    if request.user.role == 'CONTRIBUTOR':
        profile = ContributorProfile.objects.filter(user=request.user).first()
    else:
        messages.warning(request, 'Unauthorized action. Must be an Admin or Contributor')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CreateContent(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']

            cont = Content(user=request.user,
                           title=title,
                           description=description,
                           content=content)
            cont.save()
            messages.success(request, 'Content added sucessfully')
            return redirect('dashboard')
    else:
        form = CreateContent()

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'content/create_content.html', context=context)


@login_required
def explore(request):
    contents = Content.objects.all()
    contributors = ContributorProfile.objects.all()

    if len(contents) == 0:
        contents = None

    if request.user.role == 'CONTRIBUTOR':
        profile = ContributorProfile()
    elif request.user.role == 'STUDENT':
        profile = StudentProfile()

    context = {
        'contributors': contributors,
        'contents': contents,
        'profile': profile
    }

    return render(request, 'content/explore.html', context=context)

@login_required
def content_view(request, content_id):
    content = Content.objects.filter(id=content_id).first()
    contributors = ContributorProfile.objects.all()
    reviews = Review.objects.filter(content=content).all()

    if content is None:
        messages.warning(request, 'Content not found')
        return redirect('explore')

    if request.user.role == 'STUDENT':
        profile = StudentProfile()
    elif request.user.role == 'CONTRIBUTOR':
        profile = ContributorProfile()

    context = {
        'contributors': contributors,
        'content': content,
        'profile': profile,
        'reviews': reviews
    }

    return render(request, 'content/content_view.html', context=context)

@login_required
def content_update(request, content_id):
    content = Content.objects.filter(id=content_id).first()
    contr = ContributorProfile.objects.filter(user=request.user).first()

    profile = contr

    if not contr:
        messages.warning(request, 'Unauthorized: Cannot update this post')
        return redirect('content-view', content_id=content_id)

    if request.method == 'POST':
        form = UpdateContent(request.POST)
        if form.is_valid():
            content.title = form.cleaned_data['title']
            content.description = form.cleaned_data['description']
            content.content = form.cleaned_data['content']
            content.save()

            messages.success(request, 'Content updated successfully')
            return redirect('content-view', content_id=content_id)
    else:
        form = UpdateContent(instance=content)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'content/update_content.html', context=context)

@login_required
def content_delete(request, content_id):
    content = Content.objects.filter(id=content_id).first()
    contr = ContributorProfile.objects.filter(user=request.user).first()

    if content.user != contr.user:
        messages.warning(request, 'Unauthorized: Cannot delete this post')
        return redirect('content-view', content_id=content_id)

    content.delete()
    messages.success(request, 'Content deleted successfully')
    return redirect('dashboard')