from django.urls import path

from . import views

app_name = "lessons"

urlpatterns = [
    path("", views.my_learning, name="my_learning"),
    path("<slug:track_slug>/", views.track_lessons, name="track_lessons"),
    path("<slug:track_slug>/<slug:lesson_slug>/", views.lesson_detail, name="lesson_detail"),
    path("<slug:track_slug>/<slug:lesson_slug>/complete/", views.mark_lesson_complete, name="mark_lesson_complete"),
]
