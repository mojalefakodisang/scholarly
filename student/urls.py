from django.urls import path
from .views import register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", register, name="st-register"),
]