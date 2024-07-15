from django.urls import path
from .views import update_user, user_info

urlpatterns = [
    path("<str:username>/", user_info, name='user-info'),
    path("<str:username>/update", update_user, name='update-user'),
]