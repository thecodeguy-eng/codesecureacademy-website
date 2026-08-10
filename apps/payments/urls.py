from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("webhook/paystack/", views.paystack_webhook, name="paystack_webhook"),
    path("verify/<str:reference>/", views.verify_callback, name="verify_callback"),
    path("internal/release-expired-holds/", views.release_expired_holds, name="release_expired_holds"),
    path("internal/release-pending-payouts/", views.release_pending_payouts, name="release_pending_payouts"),
    path("healthz/", views.healthz, name="healthz"),
]
