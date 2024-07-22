from django.urls import path
from .views import get_notifications, notification_view, notification_delete


urlpatterns = [
    path(
        "all/",
        get_notifications,
        name='all-notifications'
    ),
    path(
        "<int:notif_id>/view/",
        notification_view,
        name='view-notification'
    ),
    path(
        "<int:notif_id>/delete/",
        notification_delete,
        name='delete-notification'
    ),
]
