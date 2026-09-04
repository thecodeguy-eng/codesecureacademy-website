from django.conf import settings

from .forms import WaitlistSignupForm
from .models import SiteSettings


def site_settings(request):
    from .services import _next_enrollment_deadline

    next_enrollment_deadline = _next_enrollment_deadline()

    return {
        "site_settings": SiteSettings.load(),
        "INSTAGRAM_URL": settings.INSTAGRAM_URL,
        "FACEBOOK_URL": settings.FACEBOOK_URL,
        "WHATSAPP_CONTACT_NUMBER": settings.WHATSAPP_CONTACT_NUMBER,
        "WHATSAPP_CHANNEL_URL": settings.WHATSAPP_CHANNEL_URL,
        "footer_waitlist_form": WaitlistSignupForm(),
        "next_enrollment_deadline": next_enrollment_deadline,
    }
