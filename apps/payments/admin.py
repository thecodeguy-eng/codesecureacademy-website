from django.contrib import admin

from .models import PaystackTransaction


@admin.register(PaystackTransaction)
class PaystackTransactionAdmin(admin.ModelAdmin):
    list_display = ("reference", "email", "amount_kobo", "status", "content_type", "object_id", "created_at")
    list_filter = ("status", "content_type")
    search_fields = ("reference", "email")
    readonly_fields = [f.name for f in PaystackTransaction._meta.fields]

    def has_add_permission(self, request):
        return False
