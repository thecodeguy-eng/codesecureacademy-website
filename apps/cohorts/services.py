from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_enrollment_receipt(enrollment):
    context = {
        "enrollment": enrollment,
        "dashboard_url": f"{settings.SITE_URL}/dashboard/",
    }
    html_body = render_to_string("emails/enrollment_receipt.html", context)
    plain_body = (
        f"Hi {enrollment.student.get_full_name() or enrollment.student.username},\n\n"
        f"Your payment went through and your seat in {enrollment.cohort.track.name} is locked in.\n\n"
        f"Track: {enrollment.cohort.track.name}\n"
        f"Cohort start date: {enrollment.cohort.start_date:%d %b %Y}\n"
        f"Amount paid: NGN{enrollment.cohort.price_naira}\n"
        f"Date paid: {enrollment.confirmed_at:%d %b %Y, %H:%M}\n\n"
        f"Your WhatsApp cohort group invite is on its way in a separate email.\n\n"
        f"Dashboard: {settings.SITE_URL}/dashboard/"
    )
    msg = EmailMultiAlternatives(
        subject=f"Payment confirmed: {enrollment.cohort.track.name}",
        body=plain_body,
        to=[enrollment.student.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=True)
