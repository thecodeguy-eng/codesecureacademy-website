from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_invite_for_enrollment(enrollment):
    """Called from Enrollment.mark_confirmed(). Emails the student their
    track's WhatsApp invite link; the same link is also shown on-screen on
    the enrollment success page."""
    from .models import TrackWhatsAppGroup

    group = TrackWhatsAppGroup.objects.filter(track=enrollment.cohort.track).first()
    if not group:
        return  # no group configured yet for this track — nothing to send

    context = {"enrollment": enrollment, "invite_link": group.invite_link}
    body = render_to_string("whatsapp/invite_email.txt", context)
    send_mail(
        subject=f"You're in! Join the {enrollment.cohort.track.name} WhatsApp group",
        message=body,
        from_email=None,  # falls back to DEFAULT_FROM_EMAIL
        recipient_list=[enrollment.student.email],
        fail_silently=True,
    )
