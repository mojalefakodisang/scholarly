from django.shortcuts import render, redirect
from .models import Review
from .forms import CreateReview, UpdateReview
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from student.models import StudentProfile
from content.models import Content
from users.utils import get_profile
from main.utils import *

@login_required
def create_review(request, content_id):
    if request.user.role == 'STUDENT':
        profile = get_profile(request)
    else:
        messages.warning(request, 'Unauthorized action: Only students can review articles')

    content = obj_by_subj(Content, 'first', id=content_id)
    
    if request.method == 'POST':
        form = CreateReview(request.POST)
        if form.is_valid():
            review_content = form.cleaned_data['review_content']
            rating = form.cleaned_data['rating']

            review = Review(content=content,
                            student=request.user,
                            review_content=review_content,
                            rating=rating)
            review.save()
            messages.success(request, 'Uploaded a review successfully')
            return redirect('content-view', content_id=content_id)
    else:
        form = CreateReview()

    context = {
        'form': form,
        'profile': profile
    }

    return render(request, 'review/create_review.html', context=context)

@login_required
def view_review(request, review_id, content_id):
    review = obj_by_subj(Review, 'first', id=review_id)

    if review is None:
        messages.warning(request, 'Review not found. Now redirecting to the content')
        return redirect('content-view', content_id=content_id)

    if review.student != request.user:
        messages.warning(request, 'Unauthorized action: Cannot update this review')
        return redirect('content-view', content_id=content_id)

    if request.method == 'POST':
        form = UpdateReview(request.POST)
        if form.is_valid():
            review.review_content = form.cleaned_data['review_content']
            review.rating = form.cleaned_data['rating']
            review.save()
            messages.success(request, 'Review updated successfully')
            return redirect('content-view', content_id=content_id)
    else:
        form = UpdateReview(instance=review)
    
    profile = get_profile(request)

    context = {
        'profile': profile,
        'review': review,
        'form': form
    }

    return render(request, 'review/view_review.html', context=context)

@login_required
def delete_review(request, review_id, content_id):
    review = obj_by_subj(Review, 'first', id=review_id)

    if review is None:
        messages.warning(request, 'Review not found')
        return redirect('content-view', content_id=content_id)
    
    if review.student != request.user:
        messages.warning(request, 'Unauthorized action: Cannot delete this review')
        return redirect('content-view', content_id=content_id)

    review.delete()
    messages.success(request, 'Review deleted successfully')
    return redirect('content-view', content_id=content_id)

@login_required
def update_review(request, review_id, content_id):
    review = obj_by_subj(Review, 'first', id=review_id)
    profile = get_profile(request)

    if review is None:
        messages.warning(request, 'Review not found')
        return redirect('content-view', content_id=content_id)

    if review.student != request.user:
        messages.warning(request, 'Unauthorized action: Cannot update this review')
        return redirect('content-view', content_id=content_id)

    if request.method == 'POST':
        form = UpdateReview(request.POST)
        if form.is_valid():
            review.review_content = form.cleaned_data['review_content']
            review.rating = form.cleaned_data['rating']
            review.save()
            messages.success(request, 'Review updated successfully')
            return redirect('content-view', content_id=content_id)
    else:
        form = UpdateReview(instance=review)

    context = {
        'form': form,
        'profile': profile
    }

    return render(request, 'review/update_review.html', context=context)
    