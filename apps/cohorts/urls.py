from django.urls import path

from . import views

app_name = "cohorts"

urlpatterns = [
    path("", views.track_list, name="track_list"),
    path("<slug:slug>/", views.track_detail, name="track_detail"),
    path("<slug:track_slug>/waitlist/", views.join_waitlist, name="join_waitlist"),
    path("checkout/<int:cohort_id>/", views.start_checkout, name="start_checkout"),
    path("enrollment/<int:enrollment_id>/success/", views.enrollment_success, name="enrollment_success"),
]
