"""
URL configuration for scholarly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from content import views as content_views
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("u/", include("users.urls")),
    path("review/", include("review.urls")),
    path("content/", include("content.urls")),
    path("student/", include("student.urls")),
    path("contributor/", include("contributor.urls")),
    path("login/", user_views.login_view, name="login"),
    path("explore/", content_views.explore, name="explore"),
    path("logout/", user_views.logout_user, name="logout"),
    path("dashboard/", user_views.dashboard, name='dashboard'),
    path("reset_request/", user_views.request_reset, name='request_reset'),
    path("reset_password/<str:username>/<str:token>/",
         user_views.reset_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
