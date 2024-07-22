"""Module that handles Notifications of a user
"""
from .models import Notifications
from review.models import Review
from django.shortcuts import render, redirect
from content.models import Content
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.utils import get_profile
from main.utils import *


@login_required
def get_notifications(request):
    """Gets all notifications of a user"""
    notifications = Notifications.objects\
        .filter(user=request.user)\
        .order_by('-created_at').all()

    profile = get_profile(request)

    context = {
        'profile': profile,
        'notifications': notifications
    }

    return render(request, 'notifications/notifications.html', context=context)


def create_notifications(request):
    """Creates a new notification for a user"""
    content = obj_by_subj(Content, 'all', user=request.user)

    for c in content:
        reviews = obj_by_subj(Review, 'all', content=c)

        if c.approved == 'Approved':
            title = f'{c.title} has been approved'
            message = f'{c.title} has been approved'

            if not obj_by_subj(
                Notifications,
                'first',
                user=request.user,
                title=title,
                message=message
            ):
                notification = obj_create(
                    Notifications,
                    user=request.user,
                    title=title,
                    message=message
                )
                notification.save()
                notification = obj_create(
                    Notifications,
                    user=request.user,
                    title=title,
                    message=message
                )
                notification.save()

        count = 0
        if reviews is None:
            count = 0
        else:
            for r in reviews:
                count += 1

        if count > 5:
            title = f'{c.title} has reached more than 10 reviews'
            message = f'{c.title} has reached more than 10 reviews'

            if not obj_by_subj(
                Notifications,
                'first',
                user=request.user,
                title=title,
                message=message
            ):

                notification = obj_create(
                    user=request.user,
                    title=title,
                    message=message
                )
                notification.save()


@login_required
def notification_view(request, notif_id):
    """Views a notification"""
    notification = obj_by_subj(
        Notifications,
        'first',
        id=notif_id,
        user=request.user
    )

    profile = get_profile(request)

    notification.read = True
    notification.save()

    context = {
        'profile': profile,
        'notification': notification
    }

    return render(request, 'notifications/notif_view.html', context=context)


@login_required
def notification_delete(request, notif_id):
    """Deletes a notification"""
    notification = obj_by_subj(
        Notifications,
        'first',
        id=notif_id,
        user=request.user
    )

    notification.delete()
    messages.success(request, 'Notification deleted successfully')

    return redirect('all-notifications')
