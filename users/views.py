from student.models import Student
from django.contrib.auth import logout
from contributor.models import Contributor
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')
    

@login_required
def dashboard(request):
    role = request.user.role
    context = {
        'role': role,
        'user': request.user
    }
    return render(request, 'users/dashboard.html', context=context)