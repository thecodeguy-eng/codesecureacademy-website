from django.contrib import admin, messages

from .models import Attendance, Instructor, SchemeTopic, Session, TopicProgress
from .services import create_instructor_login, reset_instructor_login_password, send_instructor_login_email


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "has_login", "is_active", "cohort_count")
    search_fields = ("name", "email")
    actions = ["reset_login_password"]

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new and not obj.user_id:
            user, password = create_instructor_login(obj)
            send_instructor_login_email(obj, password)
            self.message_user(
                request,
                f"Tutor login created — email: {obj.email}, password: {password} "
                "(also emailed to them; this password will not be shown again).",
                level=messages.SUCCESS,
            )

    @admin.display(description="Has login", boolean=True)
    def has_login(self, obj):
        return bool(obj.user_id)

    @admin.display(description="Cohorts")
    def cohort_count(self, obj):
        return obj.cohorts.count()

    @admin.action(description="Reset login password for selected tutors")
    def reset_login_password(self, request, queryset):
        count = 0
        for instructor in queryset:
            had_login = bool(instructor.user_id)
            password = create_instructor_login(instructor)[1] if not had_login else reset_instructor_login_password(instructor)
            send_instructor_login_email(instructor, password, is_reset=had_login)
            count += 1
        self.message_user(request, f"Reset and emailed new passwords for {count} tutor(s).")


@admin.register(SchemeTopic)
class SchemeTopicAdmin(admin.ModelAdmin):
    list_display = ("track", "order", "title")
    list_filter = ("track",)
    search_fields = ("title",)
    ordering = ("track", "order")


@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ("cohort", "topic", "covered_by", "covered_at")
    list_filter = ("cohort__track",)
    readonly_fields = ("cohort", "topic", "covered_by", "covered_at")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("cohort", "starts_at", "label")
    list_filter = ("cohort__track",)
    readonly_fields = ("cohort", "starts_at", "label", "created_at")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("session", "student", "marked_at")
    list_filter = ("session__cohort__track",)
    readonly_fields = ("session", "student", "marked_at")
