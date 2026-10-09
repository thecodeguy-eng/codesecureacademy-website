from django.urls import path

from . import views

urlpatterns = [
    path("r/<slug:code>/", views.referral_link, name="referral_link"),
    path("partner/dashboard/", views.partner_dashboard, name="partner_dashboard"),
]
