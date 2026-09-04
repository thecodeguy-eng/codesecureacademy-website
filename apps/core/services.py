import logging

from django.core import signing
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)

REMINDER_INTERVAL_DAYS = 1
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
    """Five distinct angles the campaign rotates through, so recipients
    getting this daily see a different, genuine email each time rather
    than the same "don't forget to pay" message on repeat."""
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
    ]


def _deadline_reminder_recipients():
    """Everyone worth reminding: general waitlist signups plus every
    registered user, minus anyone who already has a confirmed (paid)
    enrollment in any track (they don't need to be told to pay again),
    and minus anyone who's unsubscribed."""
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

    all_emails = waitlist_emails | user_emails
    return sorted(e for e in all_emails if e and e.lower() not in paid_emails and e.lower() not in opted_out)


def _send_variant_to(email, variant):
    html_body = render_to_string(
        "emails/campaign_email.html",
        {
            "heading": variant["heading"],
            "paragraphs": variant["paragraphs"],
            "cta_url": variant["cta_url"],
            "cta_label": variant["cta_label"],
            "unsubscribe_url": unsubscribe_url(email),
        },
    )
    plain_body = "\n\n".join(
        [p.replace("&#8358;", "NGN") for p in variant["paragraphs"]]
        + [f"{variant['cta_label']}: {variant['cta_url']}", "Code Secure Academy", f"Unsubscribe: {unsubscribe_url(email)}"]
    )
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

    connection = get_connection(fail_silently=True)
    connection.open()
    sent, failed = 0, 0
    processed_ids = []
    try:
        for item in chunk:
            msg = _send_variant_to(item.email, variant)
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
    """Call on every external cron ping. If a day's send is already in
    progress (queue non-empty), sends the next chunk of it. Otherwise,
    checks whether a new day's send is due and, if so, starts one: picks
    the next rotating variant, queues every current recipient for it, and
    sends the first chunk immediately. Skips entirely once there's no
    upcoming deadline left to remind anyone about."""
    from apps.core.models import ReminderQueueItem, SiteSettings

    if ReminderQueueItem.objects.exists():
        return _drain_reminder_queue()

    deadline = _next_enrollment_deadline()
    if not deadline:
        return {"skipped": "no upcoming deadline"}

    site_settings = SiteSettings.load()
    last_sent = site_settings.last_deadline_reminder_sent_at
    if not force and last_sent and timezone.now() - last_sent < timezone.timedelta(days=REMINDER_INTERVAL_DAYS):
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
    site_settings.save(update_fields=["last_deadline_reminder_sent_at", "last_deadline_reminder_variant"])

    logger.info("New reminder cycle started: variant=%s, %s recipients queued", variant_index, len(recipients))
    return _drain_reminder_queue()
