from django.contrib import admin

from .models import Partner, ReferralAttribution, ReferralCommission


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "referral_code", "email", "enrollment_commission_percent", "marketplace_commission_percent", "is_active", "referred_count", "referral_link_display")
    search_fields = ("name", "email", "referral_code")
    readonly_fields = ("referral_link_display",)

    @admin.display(description="Referrals")
    def referred_count(self, obj):
        return obj.referred_users.count()

    @admin.display(description="Referral link")
    def referral_link_display(self, obj):
        return obj.referral_url if obj.pk else "(save first)"


@admin.register(ReferralCommission)
class ReferralCommissionAdmin(admin.ModelAdmin):
    list_display = ("partner", "kind", "source_amount_naira", "commission_percent", "commission_amount_naira", "status", "created_at")
    list_filter = ("status", "kind", "partner")
    actions = ["mark_as_paid"]
    readonly_fields = ("partner", "kind", "content_type", "object_id", "source_amount_naira", "commission_percent", "commission_amount_naira", "created_at")

    @admin.action(description="Mark selected commissions as paid")
    def mark_as_paid(self, request, queryset):
        count = 0
        for commission in queryset.exclude(status=ReferralCommission.Status.PAID):
            commission.mark_paid()
            count += 1
        self.message_user(request, f"Marked {count} commission(s) as paid.")


@admin.register(ReferralAttribution)
class ReferralAttributionAdmin(admin.ModelAdmin):
    list_display = ("user", "partner", "created_at")
    list_filter = ("partner",)
    search_fields = ("user__email", "user__username")
