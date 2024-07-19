"""Module for Contributor urls"""
from django.urls import path
from .views import register


urlpatterns = [
    path(
        "register/",
        register,
        name="contr-register"
    ),
]
