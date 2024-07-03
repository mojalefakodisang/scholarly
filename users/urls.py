from django.urls import path
from .views import update_user

urlpatterns = [
    path("<str:username>/update", update_user, name='update-user'),
]