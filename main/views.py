"""Module for main views
"""
from django.shortcuts import render


def home(request):
    """View for the home page

    Args:
        request (HttpRequest): HttpRequest object

    Returns:
        HttpResponse: HttpResponse object
    """
    return render(request, "main/landing_page.html")
