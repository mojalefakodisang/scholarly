from django.urls import path
from .views import create_review, view_review, delete_review, update_review

urlpatterns = [
    path("<int:content_id>/new/", create_review, name="create-review"),
    path("<int:content_id>/<int:review_id>/", view_review, name="view-review"),
    path("<int:content_id>/<int:review_id>/delete", delete_review, name="delete-review"),
    path("<int:content_id>/<int:review_id>/update", update_review, name="update-review"),
]