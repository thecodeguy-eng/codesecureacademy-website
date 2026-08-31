from django.conf import settings
from django.utils import timezone

from .forms import WaitlistSignupForm
from .models import SiteSettings


def site_settings(request):
    from apps.cohorts.models import Cohort

    next_enrollment_deadline = (
        Cohort.objects.filter(
            status=Cohort.Status.OPEN,
            enrollment_deadline__isnull=False,
            enrollment_deadline__gte=timezone.now().date(),
        )
        .order_by("enrollment_deadline")
        .values_list("enrollment_deadline", flat=True)
        .first()
    )

    return {
        "site_settings": SiteSettings.load(),
        "INSTAGRAM_URL": settings.INSTAGRAM_URL,
        "FACEBOOK_URL": settings.FACEBOOK_URL,
        "WHATSAPP_CONTACT_NUMBER": settings.WHATSAPP_CONTACT_NUMBER,
        "WHATSAPP_CHANNEL_URL": settings.WHATSAPP_CHANNEL_URL,
        "footer_waitlist_form": WaitlistSignupForm(),
        "next_enrollment_deadline": next_enrollment_deadline,
    }
