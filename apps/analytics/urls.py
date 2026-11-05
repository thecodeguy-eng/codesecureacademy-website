from django.urls import path

from . import views

app_name = "analytics"

urlpatterns = [
    path("", views.insights, name="insights"),
    path("blast/", views.send_blast_view, name="send_blast"),
]
