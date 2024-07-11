from django.urls import path
from .views import create_content, content_view, content_update, content_delete, save_content, unsave_content, contributor_content

urlpatterns = [
    path("new/", create_content, name="create-content"),
    path("<int:content_id>/view", content_view, name="content-view"),
    path("<int:content_id>/update", content_update, name="content-update"),
    path("<int:content_id>/delete", content_delete, name="content-delete"),
    path("<int:content_id>/save", save_content, name="content-save"),
    path("<int:saved_id>/<int:content_id>/unsave", unsave_content, name="content-unsave"),
    path("<str:username>/content/", contributor_content, name="contributor-content"),
]