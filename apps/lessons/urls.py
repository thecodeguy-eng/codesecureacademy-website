from django.urls import path

from . import views

app_name = "lessons"

urlpatterns = [
    path("", views.lessons_home, name="lessons_home"),
    path("<slug:track_slug>/", views.lesson_list, name="lesson_list"),
    path("<slug:track_slug>/<slug:lesson_slug>/", views.lesson_detail, name="lesson_detail"),
    path("<slug:track_slug>/<slug:lesson_slug>/complete/", views.mark_complete, name="mark_complete"),
]
