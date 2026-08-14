from django.urls import path

from . import views

app_name = "accounts_extra"

urlpatterns = [
    path("resend-confirmation/", views.resend_confirmation_email, name="resend_confirmation"),
]
