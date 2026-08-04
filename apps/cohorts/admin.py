from django.contrib import admin

from .models import Cohort, Enrollment, Track, Waitlist


class CohortInline(admin.TabularInline):
    model = Cohort
    extra = 0
    fields = ("start_date", "end_date", "price_naira", "seat_count", "status")
    readonly_fields = ()


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CohortInline]


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ("track", "start_date", "end_date", "price_naira", "seat_count", "seats_taken_display", "status")
    list_filter = ("track", "status")

    @admin.display(description="Seats taken")
    def seats_taken_display(self, obj):
        return f"{obj.seats_taken}/{obj.seat_count}"


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "cohort", "status", "seat_held_at", "grace_extended_until", "confirmed_at")
    list_filter = ("status", "cohort__track")
    search_fields = ("student__username", "student__email")
    readonly_fields = ("created_at",)


@admin.register(Waitlist)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ("student", "track", "joined_at", "notified_at")
    list_filter = ("track",)
