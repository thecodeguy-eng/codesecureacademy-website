from django.urls import path

from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.listing_list, name="listing_list"),
    path("sell/apply/", views.apply_seller, name="apply_seller"),
    path("sell/dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("sell/payment-info/", views.setup_payment_info, name="setup_payment_info"),
    path("sell/listings/new/", views.create_listing, name="create_listing"),
    path("order/<int:order_id>/success/", views.order_success, name="order_success"),
    path("<slug:slug>/checkout/", views.start_checkout, name="start_checkout"),
    path("<slug:slug>/", views.listing_detail, name="listing_detail"),
]
