import logging

from django.core import signing
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)

REMINDER_SENDS_PER_DAY = 3
REMINDER_BURST_DAYS = 7
REMINDER_BURST_TOTAL_SENDS = REMINDER_SENDS_PER_DAY * REMINDER_BURST_DAYS  # 21
REMINDER_SEND_INTERVAL = timezone.timedelta(hours=24 / REMINDER_SENDS_PER_DAY)  # 8h apart
REMINDER_CHUNK_SIZE = 15
TRACKS_URL = "https://codesecureacademy.com/tracks/"
TUTORIALS_URL = "https://codesecureacademy.com/tutorials/"


def unsubscribe_url(email):
    token = signing.dumps(email, salt="email-unsubscribe")
    return f"https://codesecureacademy.com/unsubscribe/{token}/"


def _next_enrollment_deadline():
    from apps.cohorts.models import Cohort

    return (
        Cohort.objects.filter(
            status=Cohort.Status.OPEN,
            enrollment_deadline__isnull=False,
            enrollment_deadline__gte=timezone.now().date(),
        )
        .order_by("enrollment_deadline")
        .values_list("enrollment_deadline", flat=True)
        .first()
    )


def _reminder_variants(deadline_display):
    """Seven distinct angles the campaign rotates through. At three sends a
    day for a week that's 21 emails per person, so variety matters more
    here than it would for a slower campaign — every variant also gets a
    real, freshly-computed "days left" line injected at send time (see
    _drain_reminder_queue), not just a different subject line."""
    return [
        {
            "subject": f"Enrollment closes {deadline_display}, spots are limited",
            "heading": f"Enrollment closes {deadline_display}",
            "paragraphs": [
                "This is a reminder that enrollment for the current cohorts at Code Secure Academy closes soon. After that date, spots are no longer available for this round.",
                "Frontend Development, Backend Development, Cybersecurity, and Graphic Design are all open right now for &#8358;5,000. Pick a track and lock in your seat before enrollment closes.",
            ],
            "cta_url": TRACKS_URL,
            "cta_label": "Choose Your Track",
        },
        {
            "subject": "Why a cohort beats another course you'll never finish",
            "heading": "You bought courses before. Did you finish them?",
            "paragraphs": [
                "Most online courses are built to be sold, not finished. No deadline means no urgency, and no urgency means the course sits unfinished in a tab you never open again.",
                "A cohort is different. Real dates, real deadlines, and a WhatsApp community learning the same track on the same timeline, holding each other to it. That structure is the whole reason people actually finish.",
            ],
            "cta_url": TRACKS_URL,
            "cta_label": "See the Tracks",
        },
        {
            "subject": "Try it free before you pay anything",
            "heading": "You don't have to take our word for it",
            "paragraphs": [
                "Before you commit to a track, you can try the real thing for free. Our interactive tutorials let you edit real code and see it run live in your browser, no sign up required.",
                "It's the same hands-on approach every paid track is built on. If you like how it feels to actually build something instead of just watching a video, you'll like the cohort even more.",
            ],
            "cta_url": TUTORIALS_URL,
            "cta_label": "Try It Free",
        },
        {
            "subject": "Here's exactly what you get when you enroll",
            "heading": "What's included with every cohort",
            "paragraphs": [
                "A project-based curriculum, not a video playlist. Direct WhatsApp access to your cohort the moment payment clears. Fixed dates with a real deadline, not a self-paced course you'll never finish.",
                "Plus a moderated community, so there's no bad-faith noise, and track-specific tooling, the same tools and workflow used on the job. All for &#8358;5,000, and enrollment is still open right now.",
            ],
            "cta_url": TRACKS_URL,
            "cta_label": "Explore Tracks",
        },
        {
            "subject": f"Spots are going, enrollment closes {deadline_display}",
            "heading": "Don't miss this cohort",
            "paragraphs": [
                f"Enrollment for Frontend Development, Backend Development, Cybersecurity, and Graphic Design closes on {deadline_display}. Once that date passes, you'll need to wait for the next round to open.",
                "If you've been meaning to enroll, this is the reminder to actually do it. It takes a few minutes to pick a track and lock in your seat.",
            ],
            "cta_url": TRACKS_URL,
            "cta_label": "Enroll Now",
        },
        {
            "subject": "A quick note from the people building this",
            "heading": "Why we built Code Secure Academy",
            "paragraphs": [
                "We started this because too much online education ends the same way, a finished playlist, a certificate nobody asks for, and no actual project to show for it.",
                "A cohort changes that. Fixed dates, a group of people on the same timeline, and a track that ends with something you actually built yourself. That's the whole idea, and it's still open for this round.",
            ],
            "cta_url": TRACKS_URL,
            "cta_label": "See the Tracks",
        },
        {
            "subject": "Answers before you ask, laptop, payment, refunds",
            "heading": "What to know before you enroll",
            "paragraphs": [
                "A few things people usually ask before joining. Payment is by bank transfer, USSD, or card, whichever is easiest for you, right on the track page. Laptop requirements vary a bit by track, the track page has the specifics for yours.",
                "Once you're in, you get direct WhatsApp access to your cohort, real project work, and fixed dates that keep things moving. &#8358;5,000 per track, enrollment still open right now.",
            ],
            "cta_url": TRACKS_URL,
            "cta_label": "View Track Details",
        },
        {
            "personal": True,
            "sender_name": "Victory Ugochukwu",
            "sender_title": "Founder & CEO, Code Secure Academy",
            "sign_off": "Talk soon,",
            "subject_named": "{first_name}, quick note from Victory",
            "subject_anonymous": "A quick note from our founder",
            "paragraphs": [
                "I'm Victory, founder of Code Secure Academy. I noticed you signed up but haven't enrolled in a track yet, and wanted to check in myself instead of leaving it to another automated email.",
                f"If something's holding you back, cost, timing, or just not being sure which track fits, reply and tell me directly, I read these myself. If you're ready, you can see the four tracks here: {TRACKS_URL}",
            ],
        },
    ]


def _brevo_blocked_emails():
    """Addresses Brevo itself has suppressed (hard bounces, spam
    complaints). Repeatedly trying to send to an address Brevo has already
    blocked doesn't just fail quietly, it's the kind of thing that can
    degrade sender reputation for every other email this account sends,
    receipts and password resets included. Best-effort: a flaky response
    here should never block the whole campaign, so any failure just means
    "nothing known to skip" rather than an error."""
    import requests
    from django.conf import settings

    try:
        resp = requests.get(
            "https://api.brevo.com/v3/smtp/blockedContacts",
            params={"limit": 50},
            headers={"api-key": settings.BREVO_API_KEY, "Accept": "application/json"},
            timeout=15,
        )
        if resp.status_code != 200:
            return set()
        return {c["email"].lower() for c in resp.json().get("contacts", [])}
    except Exception:
        logger.warning("Could not fetch Brevo's blocked-contacts list, skipping that filter this run.", exc_info=True)
        return set()


def _deadline_reminder_recipients():
    """Everyone worth reminding: general waitlist signups plus every
    registered user, minus anyone who already has a confirmed (paid)
    enrollment in any track (they don't need to be told to pay again),
    minus anyone who's unsubscribed, and minus anyone Brevo has already
    blocked (hard bounce or spam complaint) — see _brevo_blocked_emails."""
    from django.contrib.auth import get_user_model

    from apps.cohorts.models import Enrollment
    from apps.core.models import EmailOptOut, WaitlistSignup

    User = get_user_model()

    waitlist_emails = set(WaitlistSignup.objects.values_list("email", flat=True))
    user_emails = set(User.objects.exclude(email="").values_list("email", flat=True))
    paid_emails = {
        e.lower()
        for e in Enrollment.objects.filter(status=Enrollment.Status.CONFIRMED).values_list(
            "student__email", flat=True
        )
    }
    opted_out = {e.lower() for e in EmailOptOut.objects.values_list("email", flat=True)}
    blocked = _brevo_blocked_emails()

    all_emails = waitlist_emails | user_emails
    excluded = paid_emails | opted_out | blocked
    return sorted(e for e in all_emails if e and e.lower() not in excluded)


def _days_left_display(deadline):
    if not deadline:
        return None
    days = (deadline - timezone.now().date()).days
    if days <= 0:
        return None
    if days == 1:
        return "1 day left to enroll"
    return f"{days} days left to enroll"


def _first_names_for(emails):
    """Best-effort first-name lookup for a batch of addresses, for the
    personal-note variant. Waitlist-only addresses (no account) have no
    name on file at all — those get a graceful "there" instead of "Hi
    None,". One query for the whole chunk rather than one per recipient."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    rows = User.objects.filter(email__in=emails).exclude(first_name="").values_list("email", "first_name")
    return {email.lower(): name for email, name in rows}


def _send_variant_to(email, variant, days_left_display, first_name=None):
    if variant.get("personal"):
        greeting_name = first_name or "there"
        subject = (
            variant["subject_named"].format(first_name=first_name)
            if first_name else variant["subject_anonymous"]
        )
        html_body = render_to_string(
            "emails/personal_note.html",
            {
                "first_name": greeting_name,
                "paragraphs": variant["paragraphs"],
                "sign_off": variant["sign_off"],
                "sender_name": variant["sender_name"],
                "sender_title": variant["sender_title"],
                "unsubscribe_url": unsubscribe_url(email),
            },
        )
        plain_body = "\n\n".join(
            [f"Hi {greeting_name},"] + variant["paragraphs"]
            + [variant["sign_off"], f"{variant['sender_name']}\n{variant['sender_title']}", f"Unsubscribe: {unsubscribe_url(email)}"]
        )
        msg = EmailMultiAlternatives(
            subject, plain_body, to=[email],
            from_email=f"{variant['sender_name']} <info@codesecureacademy.com>",
            reply_to=["info@codesecureacademy.com"],
        )
        msg.attach_alternative(html_body, "text/html")
        return msg

    html_body = render_to_string(
        "emails/campaign_email.html",
        {
            "heading": variant["heading"],
            "paragraphs": variant["paragraphs"],
            "cta_url": variant["cta_url"],
            "cta_label": variant["cta_label"],
            "unsubscribe_url": unsubscribe_url(email),
            "days_left_display": days_left_display,
        },
    )
    plain_parts = [p.replace("&#8358;", "NGN") for p in variant["paragraphs"]]
    if days_left_display:
        plain_parts.insert(0, days_left_display.upper())
    plain_parts += [f"{variant['cta_label']}: {variant['cta_url']}", "Code Secure Academy", f"Unsubscribe: {unsubscribe_url(email)}"]
    plain_body = "\n\n".join(plain_parts)
    msg = EmailMultiAlternatives(variant["subject"], plain_body, to=[email])
    msg.attach_alternative(html_body, "text/html")
    return msg


def _drain_reminder_queue(chunk_size=REMINDER_CHUNK_SIZE):
    """Sends the next small chunk of whatever's left in the queue for the
    day's already-chosen variant. Deliberately request-sized (not "send
    everyone") — a mass send inside one HTTP request reliably exceeds the
    platform's request timeout, so the full list drains across however
    many pings it takes, usually just a couple minutes given how often
    the external pinger hits this."""
    from apps.core.models import ReminderQueueItem

    chunk = list(ReminderQueueItem.objects.order_by("id")[:chunk_size])
    if not chunk:
        return {"skipped": "queue empty"}

    variant_index = chunk[0].variant_index
    deadline = _next_enrollment_deadline()
    deadline_display = f"{deadline:%B} {deadline.day}, {deadline.year}" if deadline else "soon"
    variant = _reminder_variants(deadline_display)[variant_index]
    days_left_display = _days_left_display(deadline)
    first_names = _first_names_for([item.email for item in chunk]) if variant.get("personal") else {}

    connection = get_connection(fail_silently=True)
    connection.open()
    sent, failed = 0, 0
    processed_ids = []
    try:
        for item in chunk:
            msg = _send_variant_to(item.email, variant, days_left_display, first_names.get(item.email.lower()))
            msg.connection = connection
            ok = msg.send(fail_silently=True)
            processed_ids.append(item.id)
            if ok:
                sent += 1
            else:
                failed += 1
    finally:
        connection.close()

    ReminderQueueItem.objects.filter(id__in=processed_ids).delete()
    remaining = ReminderQueueItem.objects.count()
    logger.info("Reminder queue chunk sent: %s ok, %s failed, %s remaining, variant=%s", sent, failed, remaining, variant_index)
    return {"sent": sent, "failed": failed, "remaining_in_queue": remaining, "variant": variant_index}


def send_deadline_reminder_if_due(force=False):
    """Call on every external cron ping. If a send is already mid-drain
    (queue non-empty), sends the next chunk of it. Otherwise, runs a
    bounded push: REMINDER_SENDS_PER_DAY sends a day for REMINDER_BURST_DAYS
    days (REMINDER_BURST_TOTAL_SENDS total), spaced REMINDER_SEND_INTERVAL
    apart, rotating through _reminder_variants. Stops automatically once
    the push completes its full run — it does not restart itself; call
    with force=True to begin a new push. Skips entirely once there's no
    upcoming deadline left to remind anyone about."""
    from apps.core.models import ReminderQueueItem, SiteSettings

    if ReminderQueueItem.objects.exists():
        return _drain_reminder_queue()

    deadline = _next_enrollment_deadline()
    if not deadline:
        return {"skipped": "no upcoming deadline"}

    site_settings = SiteSettings.load()

    if force:
        # Explicit restart: begin a fresh bounded push regardless of where
        # the previous one left off.
        site_settings.reminder_campaign_started_at = timezone.now()
        site_settings.reminder_campaign_sends_done = 0
    elif site_settings.reminder_campaign_sends_done >= REMINDER_BURST_TOTAL_SENDS:
        return {"skipped": "push complete", "sends_done": site_settings.reminder_campaign_sends_done}
    elif not site_settings.reminder_campaign_started_at:
        site_settings.reminder_campaign_started_at = timezone.now()

    last_sent = site_settings.last_deadline_reminder_sent_at
    if not force and last_sent and timezone.now() - last_sent < REMINDER_SEND_INTERVAL:
        return {"skipped": "not due yet", "last_sent": last_sent}

    variants_count = len(_reminder_variants("placeholder"))
    variant_index = (site_settings.last_deadline_reminder_variant + 1) % variants_count
    recipients = _deadline_reminder_recipients()

    from apps.core.models import ReminderQueueItem as _RQI

    _RQI.objects.bulk_create([_RQI(email=e, variant_index=variant_index) for e in recipients])

    # Marked as "sent" now, at cycle-start, not once the queue finishes
    # draining — otherwise the due-check above would see no recent send
    # while a multi-ping drain is still in progress and start a second
    # cycle on top of the first.
    site_settings.last_deadline_reminder_sent_at = timezone.now()
    site_settings.last_deadline_reminder_variant = variant_index
    site_settings.reminder_campaign_sends_done += 1
    site_settings.save(update_fields=[
        "last_deadline_reminder_sent_at", "last_deadline_reminder_variant",
        "reminder_campaign_started_at", "reminder_campaign_sends_done",
    ])

    logger.info(
        "New reminder send started (%s/%s of this push): variant=%s, %s recipients queued",
        site_settings.reminder_campaign_sends_done, REMINDER_BURST_TOTAL_SENDS, variant_index, len(recipients),
    )
    return _drain_reminder_queue()
