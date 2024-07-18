"""Views module for content model"""
from review.models import Review
from django.contrib import messages
from student.models import StudentProfile
from .models import Content, SavedContent
from django.shortcuts import render, redirect
from .forms import CreateContent, UpdateContent
from django.contrib.auth.decorators import login_required
from contributor.models import ContributorProfile
from moderator.models import ModeratorProfile
from review.forms import CreateReview, UpdateReview
from users.models import User


def get_profile(request):
    """Gets the profile of the logged in user"""
    if request.user.role == 'STUDENT':
        return StudentProfile.objects.filter(user=request.user).first()
    elif request.user.role == 'CONTRIBUTOR':
        return ContributorProfile.objects.filter(user=request.user).first()
    elif request.user.role == 'MODERATOR':
        return ModeratorProfile.objects.filter(user=request.user).first()


@login_required
def create_content(request):
    """Create content view function

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse object
    """
    if request.user.role == 'CONTRIBUTOR':
        profile = ContributorProfile.objects.filter(user=request.user).first()
    else:
        messages.warning(
            request,
            'Unauthorized action. Must be an Admin or Contributor'
        )
        return redirect('dashboard')

    if request.method == 'POST':
        form = CreateContent(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']
            categories = form.cleaned_data['categories_str']

            cont = Content(user=request.user, categories_str=categories,
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
        'path': request.path
    }
    return render(request, 'content/create_content.html', context=context)


@login_required
def explore(request):
    """Explore view function

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse object
    """
    contents = Content.objects.all()
    contributors = ContributorProfile.objects.all()

    if request.user.role == 'STUDENT':
        saved = SavedContent.objects.filter(student=request.user).first()
    else:
        saved = None

    if len(contents) == 0:
        contents = None

    profile = get_profile(request)

    student_content = []
    if contents is None:
        student_content = None
    else:
        for c in contents:
            if c.approved == 'Approved':
                student_content.append(c)

        if len(student_content) == 0:
            student_content = None

    context = {
        'path': request.path,
        'c_profiles': contributors,
        'contents': contents,
        'profile': profile,
        'saved': saved,
        'student_content': student_content
    }

    return render(request, 'content/explore.html', context=context)


@login_required
def content_view(request, content_id):
    """Content view function

    Args:
        request: HttpRequest object
        content_id: int

    Returns:
        HttpResponse object
    """
    content = Content.objects.filter(id=content_id).first()
    contributors = ContributorProfile.objects.all()
    reviews = Review.objects.filter(content=content).all()
    saved = SavedContent.objects.filter(
        content=content_id,
        student=request.user).first()
    categories = content.categories.all()

    if content is None:
        messages.warning(request, 'Content not found')
        return redirect('explore')

    profile = get_profile(request)

    if len(reviews) == 0:
        reviews = None

    if request.method == 'POST':
        form = CreateReview(request.POST)
        if form.is_valid():
            rev = form.cleaned_data['review_content']
            rating = form.cleaned_data['rating']
            review = Review(
                student=request.user,
                content=content,
                review_content=rev,
                rating=rating)

            review.save()
            messages.success(request, 'Review posted successfully')
            return redirect('content-view', content_id=content_id)
        else:
            messages.warning(request, 'Unable to post Review')
            return redirect('content-view', content_id=content_id)
    else:
        form = CreateReview()

    context = {
        'contributors': contributors,
        'categories': categories,
        'path': request.path,
        'content': content,
        'profile': profile,
        'reviews': reviews,
        'saved': saved,
        'form': form
    }

    return render(request, 'content/content_view.html', context=context)


@login_required
def content_update(request, content_id):
    """Content update view function

    Args:
        request: HttpRequest object
        content_id: int

    Returns:
        HttpResponse object
    """
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
            content.categories_str = form.cleaned_data['categories_str']
            content.approve = 'Pending'
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
    """Content delete view function

    Args:
        request: HttpRequest object
        content_id: int

    Returns:
        HttpResponse object
    """
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
    """Content save view function

    Args:
        request: HttpRequest object
        content_id: int

    Returns:
        HttpResponse object
    """
    existing = SavedContent.objects.filter(
        content=content_id,
        student=request.user).first()

    if existing:
        return redirect(
            'content-unsave',
            content_id=content_id,
            saved_id=existing.id
        )

    content = Content.objects.get(id=content_id)

    if not content:
        messages.warning(request, 'Content not found')

    if request.user.role != 'STUDENT':
        messages.warning(
            request,
            'Unauthorized action: Only Students can save contents'
        )
        return redirect('explore')

    saved_content = SavedContent(content=content, student=request.user)
    saved_content.save()
    messages.success(request, 'Content successfully saved')
    return redirect('explore')


@login_required
def unsave_content(request, content_id, saved_id):
    """Content unsave view function

    Args:
        request: HttpRequest object
        content_id: int
        saved_id: int

    Returns:
        HttpResponse object
    """
    existing = SavedContent.objects.filter(id=saved_id).first()

    if existing is None:
        return redirect('save-content', content_id=content_id)

    existing.delete()
    messages.success(request, 'Content unsaved successfully')
    return redirect('explore')


@login_required
def contributor_content(request, username):
    """Contributor content view function

    Args:
        request: HttpRequest object
        username: str

    Returns:
        HttpResponse object
    """
    user = User.objects.filter(username=username).first()
    contents = Content.objects.filter(user=user).all()

    profile = ContributorProfile.objects.filter(user=request.user).first()

    context = {
        'profile': profile,
        'contents': contents
    }

    return render(request, 'content/contr_content.html', context=context)
