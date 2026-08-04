from django.conf import settings

from .models import SiteSettings


def site_settings(request):
    return {
        "site_settings": SiteSettings.load(),
        "INSTAGRAM_URL": settings.INSTAGRAM_URL,
        "FACEBOOK_URL": settings.FACEBOOK_URL,
        "WHATSAPP_CONTACT_NUMBER": settings.WHATSAPP_CONTACT_NUMBER,
    }
