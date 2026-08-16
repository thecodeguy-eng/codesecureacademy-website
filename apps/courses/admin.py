from django.contrib import admin

from .models import Course, CourseModule, LiveSession, Payout, Purchase, Tutor


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "phone_number", "status", "applied_at")
    list_filter = ("status",)
    actions = ["approve_tutors", "reject_tutors"]

    @admin.action(description="Approve selected tutors")
    def approve_tutors(self, request, queryset):
        for tutor in queryset:
            tutor.approve()

    @admin.action(description="Reject selected tutors")
    def reject_tutors(self, request, queryset):
        queryset.update(status=Tutor.Status.REJECTED)


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1


class LiveSessionInline(admin.TabularInline):
    model = LiveSession
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "tutor", "delivery_type", "price_naira", "status", "created_at")
    list_filter = ("status", "delivery_type")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CourseModuleInline, LiveSessionInline]
    actions = ["approve_courses", "reject_courses"]

    @admin.action(description="Approve selected courses")
    def approve_courses(self, request, queryset):
        queryset.update(status=Course.Status.ACTIVE)

    @admin.action(description="Reject selected courses")
    def reject_courses(self, request, queryset):
        queryset.update(status=Course.Status.REJECTED)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "amount_naira", "status", "created_at", "paid_at")
    list_filter = ("status",)
    readonly_fields = ("created_at",)


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    """Payouts release automatically once they've sat `PAYOUT_HOLD_HOURS`
    (see apps.payments.views.release_pending_payouts, hit by the same
    external cron pinger as release_expired_holds) — this action is for
    urgent one-offs. To hold one back from the automatic sweep, just leave
    it alone; it only ever touches rows still `status=pending`."""

    list_display = ("tutor", "purchase", "amount_naira", "status", "created_at", "paid_at")
    list_filter = ("status",)
    readonly_fields = ("created_at",)
    actions = ["release_now"]

    @admin.action(description="Release selected payouts now (real Paystack transfer)")
    def release_now(self, request, queryset):
        for payout in queryset:
            payout.release()
