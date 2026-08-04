from django.contrib import admin
from django.utils import timezone

from .models import Listing, Order, Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("business_name", "user", "category", "status", "applied_at")
    list_filter = ("status", "category")
    actions = ["approve_sellers", "reject_sellers"]

    @admin.action(description="Approve selected sellers (creates Paystack subaccount)")
    def approve_sellers(self, request, queryset):
        for seller in queryset:
            seller.approve()

    @admin.action(description="Reject selected sellers")
    def reject_sellers(self, request, queryset):
        queryset.update(status=Seller.Status.REJECTED)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "category", "price_naira", "status", "created_at")
    list_filter = ("status", "category")
    prepopulated_fields = {"slug": ("title",)}
    actions = ["approve_listings", "reject_listings"]

    @admin.action(description="Approve selected listings")
    def approve_listings(self, request, queryset):
        queryset.update(status=Listing.Status.ACTIVE)

    @admin.action(description="Reject selected listings")
    def reject_listings(self, request, queryset):
        queryset.update(status=Listing.Status.REJECTED)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("buyer", "listing", "amount_naira", "status", "created_at", "paid_at")
    list_filter = ("status",)
    readonly_fields = ("created_at",)
