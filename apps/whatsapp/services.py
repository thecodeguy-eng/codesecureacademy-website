import logging

from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_invite_for_enrollment(enrollment):
    """Called from Enrollment.mark_confirmed(). Emails the student their
    track's WhatsApp invite link; the same link is also shown on-screen on
    the enrollment success page."""
    from .models import TrackWhatsAppGroup

    group = TrackWhatsAppGroup.objects.filter(track=enrollment.cohort.track).first()
    if not group:
        # A student just paid for a track with no WhatsApp group set up —
        # they get no community invite at all until someone notices and
        # configures one. That's a real gap, not a quiet edge case, so it
        # goes to the same admin-alert pipeline as an application error.
        logger.error(
            "Enrollment %s confirmed for %s (%s) but no WhatsApp group is configured for track %r — "
            "the student got no community invite. Add one in the admin.",
            enrollment.id, enrollment.student.email, enrollment.student.get_full_name(), enrollment.cohort.track.name,
        )
        return

    context = {"enrollment": enrollment, "invite_link": group.invite_link}
    body = render_to_string("whatsapp/invite_email.txt", context)
    send_mail(
        subject=f"You're in! Join the {enrollment.cohort.track.name} WhatsApp group",
        message=body,
        from_email=None,  # falls back to DEFAULT_FROM_EMAIL
        recipient_list=[enrollment.student.email],
        fail_silently=True,
    )
