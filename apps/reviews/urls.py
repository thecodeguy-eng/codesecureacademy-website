from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("submit/<str:app_label>/<str:model_name>/<int:object_id>/", views.submit_review, name="submit_review"),
]
