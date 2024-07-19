from .models import Notifications
from review.models import Review
from django.shortcuts import render, redirect
from content.models import Content, ModeratedContent
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from student.models import StudentProfile
from contributor.models import ContributorProfile
from moderator.models import ModeratorProfile
from users.utils import get_profile

@login_required
def get_notifications(request):
    notifications = Notifications.objects.filter(user=request.user).order_by('-created_at').all()

    profile = get_profile(request)

    context = {
        'profile': profile,
        'notifications': notifications
    }
    
    return render(request, 'notifications/notifications.html', context=context)

def create_notifications(request):
    content = Content.objects.filter(user=request.user).all()
    
    for c in content:
        reviews = Review.objects.filter(content=c).all()

        if c.approved == 'Approved':
            title = f'{c.title} has been approved'
            message = f'{c.title} has been approved'
            
            if not Notifications.objects.filter(user=request.user, title=title,
                                                message=message).exists():
                
                notification = Notifications.objects.create(user=request.user,
                                                            title=title,
                                                            message=message)
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
            
            if not Notifications.objects.filter(user=request.user, title=title,
                                                message=message).exists():
                
                notification = Notifications.objects.create(user=request.user,
                                                            title=title,
                                                            message=message)
                notification.save()

@login_required
def notification_view(request, notif_id):
    notification = Notifications.objects.filter(id=notif_id, user=request.user).first()

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
    notification = Notifications.objects.filter(id=notif_id, user=request.user).first()

    notification.delete()
    messages.success(request, 'Notification deleted successfully')

    return redirect('all-notifications')