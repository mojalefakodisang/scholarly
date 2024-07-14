from django.shortcuts import render


def home(request):
    return render(request, "main/landing_page.html")