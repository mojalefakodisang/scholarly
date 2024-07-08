from django.urls import path
from .views import register, approve_content, disapprove_content

urlpatterns = [
    path("register/", register, name="mod-register"),
    path("<int:content_id>/approve/", approve_content, name='approve'),
    path("<int:content_id>/disapprove/", disapprove_content, name='disapprove'),
]