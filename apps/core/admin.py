from django.contrib import admin

from .admin_mixins import BroadcastEmailAdminMixin
from .models import FAQ, SiteSettings, WaitlistSignup


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("students_trained", "cohorts_run", "hiring_partners")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)


@admin.register(WaitlistSignup)
class WaitlistSignupAdmin(BroadcastEmailAdminMixin, admin.ModelAdmin):
    list_display = ("email", "joined_at", "notified_at")
    search_fields = ("email",)
    actions = ["broadcast_email"]

    def get_broadcast_email(self, obj):
        return obj.email
