from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "phone_number", "track_of_interest", "is_email_verified_display", "is_staff")
    list_filter = ("track_of_interest", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("CSA profile", {"fields": ("phone_number", "track_of_interest")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("CSA profile", {"fields": ("email", "phone_number", "track_of_interest")}),
    )

    @admin.display(boolean=True, description="Email verified")
    def is_email_verified_display(self, obj):
        return obj.is_email_verified
