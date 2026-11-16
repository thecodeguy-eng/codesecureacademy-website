from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Alternates which founder's name a personal note is signed with, so it
# doesn't always read as the same person reaching out. Deterministic on
# the user's own pk (not random) so a given user gets a consistent voice
# across their own welcome + enrollment notes, and re-sending (e.g. a
# retried signal) never flips the signature mid-conversation.
FOUNDERS = [
    {"sender_name": "Ibeawuchi C.N.", "sender_title": "Co-Founder & Chief Technology Officer, Code Secure Academy"},
    {"sender_name": "Victory Ugochukwu", "sender_title": "Founder & Academy Director, Code Secure Academy"},
]


def _founder_for(user):
    return FOUNDERS[user.pk % len(FOUNDERS)]


def _send_personal_note(to_email, subject, first_name, paragraphs, sign_off, founder):
    """Shared by send_welcome_note/send_enrollment_personal_note. These are
    one-off notes triggered by the recipient's own action (signing up,
    paying), not a recurring campaign — no unsubscribe link and no
    EmailOptOut check, same treatment the codebase already gives receipts
    and other transactional email (see EmailOptOut's own docstring)."""
    html_body = render_to_string(
        "emails/personal_note.html",
        {
            "first_name": first_name,
            "paragraphs": paragraphs,
            "sign_off": sign_off,
            "sender_name": founder["sender_name"],
            "sender_title": founder["sender_title"],
            "unsubscribe_url": None,
        },
    )
    plain_body = "\n\n".join(
        [f"Hi {first_name},"] + paragraphs
        + [sign_off, f"{founder['sender_name']}\n{founder['sender_title']}"]
    )
    msg = EmailMultiAlternatives(
        subject, plain_body, to=[to_email],
        from_email=f"{founder['sender_name']} <info@codesecureacademy.com>",
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=True)


def send_welcome_note(user):
    """Fired once, right after signup (see apps/accounts/signals.py) —
    alongside allauth's own "confirm your email" message, not instead of
    it. A human note, not another system email."""
    if not user.email:
        return
    founder = _founder_for(user)
    first_name = user.first_name or "there"
    site_url = settings.SITE_URL.rstrip("/")
    paragraphs = [
        "Welcome to Code Secure Academy, glad you're here.",
        f'Take a look around: <a href="{site_url}/tracks/">four tracks</a> to choose from '
        f"(Frontend Development, Backend Development, Cybersecurity, Graphic Design), or if you'd rather "
        f'just start learning something right now with no enrollment needed, our <a href="{site_url}/tutorials/">Free Tutorials</a> '
        "are open to everyone.",
        "If anything's unclear, or you just want to ask a question before picking a track, reply to this email. "
        "It reaches a real person, not a support queue.",
    ]
    subject = f"Welcome to Code Secure Academy, {user.first_name}" if user.first_name else "Welcome to Code Secure Academy"
    _send_personal_note(
        to_email=user.email, subject=subject, first_name=first_name,
        paragraphs=paragraphs, sign_off="Glad to have you here,", founder=founder,
    )


def send_enrollment_personal_note(enrollment):
    """Fired alongside send_enrollment_receipt (apps/cohorts/services.py)
    when a payment is confirmed — that one's the formal receipt with the
    payment details; this one's the human follow-up."""
    user = enrollment.student
    if not user.email:
        return
    founder = _founder_for(user)
    first_name = user.first_name or "there"
    track_name = enrollment.cohort.track.name
    paragraphs = [
        f"Just saw your payment come through for {track_name}, your seat's locked in.",
        "The formal receipt with the payment details is in a separate email. This one's just from me: "
        "looking forward to having you in the cohort.",
        "If you have any questions before things kick off, reply here directly.",
    ]
    _send_personal_note(
        to_email=user.email, subject=f"You're in: {track_name}", first_name=first_name,
        paragraphs=paragraphs, sign_off="Talk soon,", founder=founder,
    )
