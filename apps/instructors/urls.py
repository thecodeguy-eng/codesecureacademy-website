from django.urls import path

from . import views

app_name = "instructors"

urlpatterns = [
    path("tutor/dashboard/", views.instructor_dashboard, name="dashboard"),
    path("tutor/cohort/<int:cohort_id>/topic/<int:topic_id>/toggle/", views.toggle_topic, name="toggle_topic"),
    path("tutor/cohort/<int:cohort_id>/announcement/", views.update_announcement, name="update_announcement"),
    path("tutor/cohort/<int:cohort_id>/session/new/", views.create_session, name="create_session"),
    path("tutor/session/<int:session_id>/student/<int:student_id>/toggle/", views.toggle_attendance, name="toggle_attendance"),
]
