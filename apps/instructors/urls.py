from django.urls import path

from . import views

app_name = "instructors"

urlpatterns = [
    path("tutor/dashboard/", views.instructor_dashboard, name="dashboard"),
    path("tutor/cohort/<int:cohort_id>/topic/<int:topic_id>/toggle/", views.toggle_topic, name="toggle_topic"),
]
