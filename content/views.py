from review.models import Review
from django.contrib import messages
from student.models import StudentProfile
from .models import Content, SavedContent
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
            category = form.cleaned_data['category']

            cont = Content(user=request.user, category=category,
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

    if request.user.role == 'STUDENT':
        saved = SavedContent.objects.filter(student=request.user).first()
    else:
        saved = None

    if len(contents) == 0:
        contents = None

    if request.user.role == 'CONTRIBUTOR':
        profile = ContributorProfile()
    elif request.user.role == 'STUDENT':
        profile = StudentProfile()

    context = {
        'contributors': contributors,
        'contents': contents,
        'profile': profile,
        'saved': saved
    }

    return render(request, 'content/explore.html', context=context)

@login_required
def content_view(request, content_id):
    content = Content.objects.filter(id=content_id).first()
    contributors = ContributorProfile.objects.all()
    reviews = Review.objects.filter(content=content).all()
    saved = SavedContent.objects.filter(content=content_id, student=request.user).first()

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
        'reviews': reviews,
        'saved': saved
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
            content.category = form.cleaned_data['category']
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

@login_required
def save_content(request, content_id):
    existing = SavedContent.objects.filter(content=content_id, student=request.user).first()

    if existing:
        return redirect('content-unsave', content_id=content_id, saved_id=existing.id)
    
    content = Content.objects.get(id=content_id)

    if not content:
        messages.warning(request, 'Content not found')

    if request.user.role != 'STUDENT':
        messages.warning(request, 'Unauthorized action: Only Students can save contents')
        return redirect('explore')

    saved_content = SavedContent(content=content, student=request.user)
    saved_content.save()
    messages.success(request, 'Content successfully saved')
    return redirect('explore')

@login_required
def unsave_content(request, content_id, saved_id):
    existing = SavedContent.objects.filter(id=saved_id).first()

    if existing is None:
        return redirect('save-content', content_id=content_id)

    existing.delete()
    messages.success(request, 'Content unsaved successfully')
    return redirect('explore')