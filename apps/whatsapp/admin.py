from django.contrib import admin

from .models import TrackWhatsAppGroup


@admin.register(TrackWhatsAppGroup)
class TrackWhatsAppGroupAdmin(admin.ModelAdmin):
    list_display = ("track", "invite_link", "updated_at")
