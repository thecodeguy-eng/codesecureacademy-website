from django.contrib import admin, messages

from .models import Partner, ReferralAttribution, ReferralCommission
from .services import create_partner_login, reset_partner_login_password, send_partner_login_email


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "referral_code", "email", "has_login", "enrollment_commission_percent", "marketplace_commission_percent", "is_active", "referred_count", "referral_link_display")
    search_fields = ("name", "email", "referral_code")
    readonly_fields = ("referral_link_display",)
    actions = ["reset_login_password"]

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new and not obj.user_id:
            user, password = create_partner_login(obj)
            send_partner_login_email(obj, password)
            self.message_user(
                request,
                f"Partner login created — email: {obj.email}, password: {password} "
                "(also emailed to them; this password will not be shown again).",
                level=messages.SUCCESS,
            )

    @admin.display(description="Referrals")
    def referred_count(self, obj):
        return obj.referred_users.count()

    @admin.display(description="Referral link")
    def referral_link_display(self, obj):
        return obj.referral_url if obj.pk else "(save first)"

    @admin.display(description="Has login", boolean=True)
    def has_login(self, obj):
        return bool(obj.user_id)

    @admin.action(description="Reset login password for selected partners")
    def reset_login_password(self, request, queryset):
        count = 0
        for partner in queryset:
            had_login = bool(partner.user_id)
            if not had_login:
                user, password = create_partner_login(partner)
            else:
                password = reset_partner_login_password(partner)
            send_partner_login_email(partner, password, is_reset=had_login)
            count += 1
        self.message_user(request, f"Reset and emailed new passwords for {count} partner(s).")


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
