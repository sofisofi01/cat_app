from django.urls import path
from . import views

urlpatterns = [
    path("random-prediction/", views.get_random_prediction, name="random_prediction"),
    path("add-prediction/", views.add_prediction, name="add_prediction"),
    path("like-prediction/<int:prediction_id>/", views.like_prediction, name="like_prediction"),
    path("add-comment/<int:prediction_id>/", views.add_comment, name="add_comment"),
    path("upload-image/", views.upload_image, name="upload_image"),
    path("images/", views.get_all_images, name="get_all_images"),
    path("images/<int:image_id>/", views.get_image_details, name="get_image_details"),
    path("all-predictions/", views.get_all_predictions, name="get_all_predictions"),
    path("comments/<int:prediction_id>/", views.get_comments_for_prediction, name="get_comments_for_prediction"),
]