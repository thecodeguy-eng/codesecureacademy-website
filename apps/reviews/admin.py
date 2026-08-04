from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer", "rating", "status", "content_type", "object_id", "created_at")
    list_filter = ("status", "rating", "content_type")
    search_fields = ("reviewer__username", "reviewer__email", "body")
    actions = ["approve_reviews", "reject_reviews"]

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        from django.utils import timezone

        queryset.update(status=Review.Status.APPROVED, moderated_at=timezone.now())

    @admin.action(description="Reject selected reviews")
    def reject_reviews(self, request, queryset):
        from django.utils import timezone

        queryset.update(status=Review.Status.REJECTED, moderated_at=timezone.now())
