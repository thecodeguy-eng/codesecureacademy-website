from django.urls import path

from . import views

urlpatterns = [
    path("r/<slug:code>/", views.referral_link, name="referral_link"),
]
