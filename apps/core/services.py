import logging

from django.core import signing
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)

REMINDER_BURST_DAYS = 7
REMINDER_CHUNK_SIZE = 15
REMINDER_DAILY_CAP = 200  # stays well under Brevo's free-tier 300/day ceiling, leaving headroom
# for transactional mail (signup confirmations, receipts, password resets) so the campaign can
# never eat the whole quota and silently block those.
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
    """Eight distinct angles the campaign rotates through, one per batch
    cycle (see send_deadline_reminder_if_due) — every variant also gets a
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
                "A project-based curriculum you work through with your cohort. Lesson access on your dashboard the moment payment clears. Fixed dates with a real deadline, so the course doesn't sit half-finished in a tab somewhere.",
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


def brevo_account_status():
    """Live plan type + remaining daily send credits, straight from Brevo's
    own account endpoint — the one source of truth that actually distinguishes
    "we sent it" from "Brevo accepted the API call but had no quota left to
    dispatch it." Used by the admin insights dashboard so this doesn't have
    to be checked by hand again. Best-effort: returns None on any failure."""
    import requests
    from django.conf import settings

    try:
        resp = requests.get(
            "https://api.brevo.com/v3/account",
            headers={"api-key": settings.BREVO_API_KEY, "Accept": "application/json"},
            timeout=15,
        )
        if resp.status_code != 200:
            return None
        for plan in resp.json().get("plan", []):
            if plan.get("creditsType") == "sendLimit":
                return {"type": plan.get("type"), "credits_remaining": plan.get("credits")}
        return None
    except Exception:
        logger.warning("Could not check Brevo account status.", exc_info=True)
        return None


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


BLAST_AUDIENCE_CHOICES = [
    ("both", "Registered users + waitlist (everyone)"),
    ("registered", "Only registered users"),
    ("waitlist", "Only waitlist (never registered)"),
    ("staff_admin", "Only staff/admin accounts"),
    ("tutors", "Only tutors/instructors"),
]
BLAST_DEFAULT_CTA_LABEL = "Visit Code Secure Academy"
BLAST_DEFAULT_CTA_URL = "https://codesecureacademy.com/"


def blast_recipients(audience="both"):
    """Recipient list for a one-off announcement blast (see send_blast),
    for one of BLAST_AUDIENCE_CHOICES. "both"/"registered" are ordered
    oldest-signup-first; "waitlist" means people who never actually
    registered an account, so any email that IS a registered user's is
    excluded from it. Always excludes anyone who's unsubscribed or whom
    Brevo has already blocked. Unlike _deadline_reminder_recipients, this
    does NOT exclude confirmed/paid students for "both"/"registered" — an
    announcement isn't a "come pay" nag, paying students still want to
    hear about site updates."""
    from django.contrib.auth import get_user_model
    from django.db.models import Q

    from apps.core.models import EmailOptOut, WaitlistSignup
    from apps.instructors.models import Instructor

    User = get_user_model()
    excluded = {e.lower() for e in EmailOptOut.objects.values_list("email", flat=True)} | _brevo_blocked_emails()
    if audience == "waitlist":
        excluded |= {e.lower() for e in User.objects.exclude(email="").values_list("email", flat=True)}

    seen, ordered = set(), []

    def add(email):
        key = email.lower()
        if email and key not in seen and key not in excluded:
            seen.add(key)
            ordered.append(email)

    if audience == "staff_admin":
        qs = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).exclude(email="").order_by("date_joined")
        for email in qs.values_list("email", flat=True):
            add(email)
    elif audience == "tutors":
        qs = Instructor.objects.filter(is_active=True).exclude(email="").order_by("name")
        for email in qs.values_list("email", flat=True):
            add(email)
    else:
        if audience in ("both", "registered"):
            qs = User.objects.filter(is_staff=False, is_superuser=False).exclude(email="").order_by("date_joined")
            for email in qs.values_list("email", flat=True):
                add(email)
        if audience in ("both", "waitlist"):
            for email in WaitlistSignup.objects.order_by("joined_at").values_list("email", flat=True):
                add(email)

    return ordered


BLAST_QUOTA_BUFFER = 20  # held back from Brevo's live remaining-credits figure for transactional email
# (signup confirmations, receipts, password resets) that share the same daily cap.


def send_blast(blast_key, subject, raw_paragraphs, cta_label=None, cta_url=None, audience="both", batch_size=None):
    """Queues (on first call for this blast_key) and sends the next batch
    of a one-off announcement blast — used by both the send_blast
    management command and the staff "Send announcement email" dashboard
    page. Call again later with the same blast_key to resume, skipping
    anyone already attempted; batch_size=None asks for everyone still
    queued, but the actual batch sent is still capped to whatever Brevo's
    account API says is safely left today (see BLAST_QUOTA_BUFFER) — so
    leaving the limit blank, or asking for more than the day's quota
    allows, can never blow through the free-plan daily send cap and get
    the rest wrongly marked failed. Returns {"sent", "failed",
    "remaining", "queued_total", "quota_note"}."""
    from apps.core.models import BlastRecipient

    cta_label = cta_label or BLAST_DEFAULT_CTA_LABEL
    cta_url = cta_url or BLAST_DEFAULT_CTA_URL

    queued_total = BlastRecipient.objects.filter(blast_key=blast_key).count()
    if queued_total == 0:
        emails = blast_recipients(audience)
        BlastRecipient.objects.bulk_create(
            BlastRecipient(blast_key=blast_key, email=email, position=i) for i, email in enumerate(emails)
        )
        queued_total = len(emails)

    pending = BlastRecipient.objects.filter(blast_key=blast_key, sent_at__isnull=True).order_by("position")
    total_remaining = pending.count()
    requested = batch_size if batch_size else total_remaining

    quota_note = None
    status = brevo_account_status()
    if status and status.get("credits_remaining") is not None:
        safe_quota = max(status["credits_remaining"] - BLAST_QUOTA_BUFFER, 0)
        if safe_quota < requested:
            quota_note = (
                f"Capped to {safe_quota} this run to stay under today's Brevo quota "
                f"({status['credits_remaining']} credits left, {BLAST_QUOTA_BUFFER} held back for "
                f"transactional email). Come back after the quota resets to send the rest."
            )
            requested = safe_quota

    batch = list(pending[:requested]) if requested else []

    sent, failed = 0, 0
    if batch:
        from django.utils.html import escape
        from django.utils.safestring import mark_safe

        html_paragraphs = [mark_safe(escape(p).replace("\n", "<br>")) for p in raw_paragraphs]
        connection = get_connection(fail_silently=True)
        connection.open()
        try:
            for recipient in batch:
                html_body = render_to_string(
                    "emails/campaign_email.html",
                    {
                        "heading": subject,
                        "paragraphs": html_paragraphs,
                        "cta_url": cta_url,
                        "cta_label": cta_label,
                        "unsubscribe_url": unsubscribe_url(recipient.email),
                        "days_left_display": None,
                    },
                )
                plain_body = "\n\n".join(
                    raw_paragraphs
                    + [f"{cta_label}: {cta_url}", "Code Secure Academy", f"Unsubscribe: {unsubscribe_url(recipient.email)}"]
                )
                msg = EmailMultiAlternatives(subject, plain_body, to=[recipient.email])
                msg.attach_alternative(html_body, "text/html")
                msg.connection = connection
                ok = msg.send(fail_silently=True)
                recipient.sent_at = timezone.now()
                recipient.failed = not ok
                recipient.save(update_fields=["sent_at", "failed"])
                if ok:
                    sent += 1
                else:
                    failed += 1
        finally:
            connection.close()

    remaining_after = total_remaining - len(batch)
    return {
        "sent": sent, "failed": failed, "remaining": remaining_after,
        "queued_total": queued_total, "quota_note": quota_note,
    }


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
    """Call on every external cron ping. Rather than blasting every
    recipient at once, this spreads each variant's send across as many
    days as it takes, capped at REMINDER_DAILY_CAP emails/day total, so the
    campaign can never eat the whole Brevo daily quota and starve
    transactional mail. A ~380-person recipient list at a 200/day cap
    means one variant takes ~2 days to fully reach everyone before the
    next variant's batch begins — same rotating content as before, just
    grouped into safe daily batches instead of firing all at once.

    Stops automatically once REMINDER_BURST_DAYS have elapsed since the
    push started (it does not restart itself; call with force=True to
    begin a new push). Skips entirely once there's no upcoming deadline
    left to remind anyone about."""
    from apps.core.models import ReminderQueueItem, SiteSettings

    site_settings = SiteSettings.load()
    if site_settings.reminder_campaign_paused:
        return {"skipped": "campaign paused"}

    deadline = _next_enrollment_deadline()
    if not deadline:
        return {"skipped": "no upcoming deadline"}

    today = timezone.now().date()
    if site_settings.reminder_today_date != today:
        site_settings.reminder_today_date = today
        site_settings.reminder_sent_today = 0

    if force:
        # Explicit restart: begin a fresh bounded push regardless of where
        # the previous one left off, dropping any half-drained batch.
        site_settings.reminder_campaign_started_at = timezone.now()
        ReminderQueueItem.objects.all().delete()
    elif not site_settings.reminder_campaign_started_at:
        site_settings.reminder_campaign_started_at = timezone.now()

    daily_remaining = REMINDER_DAILY_CAP - site_settings.reminder_sent_today
    if daily_remaining <= 0:
        site_settings.save(update_fields=["reminder_today_date", "reminder_sent_today", "reminder_campaign_started_at"])
        return {"skipped": "daily cap reached", "sent_today": site_settings.reminder_sent_today}

    push_expired = timezone.now() - site_settings.reminder_campaign_started_at > timezone.timedelta(days=REMINDER_BURST_DAYS)
    queue_empty = not ReminderQueueItem.objects.exists()

    if queue_empty:
        if push_expired and not force:
            site_settings.save(update_fields=["reminder_today_date", "reminder_sent_today", "reminder_campaign_started_at"])
            return {"skipped": "push complete (7-day window elapsed)"}

        variants_count = len(_reminder_variants("placeholder"))
        variant_index = (site_settings.last_deadline_reminder_variant + 1) % variants_count
        recipients = _deadline_reminder_recipients()
        ReminderQueueItem.objects.bulk_create([ReminderQueueItem(email=e, variant_index=variant_index) for e in recipients])
        site_settings.last_deadline_reminder_variant = variant_index
        site_settings.last_deadline_reminder_sent_at = timezone.now()
        logger.info("New reminder cycle started: variant=%s, %s recipients queued", variant_index, len(recipients))

    result = _drain_reminder_queue(chunk_size=min(REMINDER_CHUNK_SIZE, daily_remaining))
    site_settings.reminder_sent_today += result.get("sent", 0) + result.get("failed", 0)
    site_settings.reminder_campaign_sends_done += result.get("sent", 0)
    site_settings.save(update_fields=[
        "reminder_today_date", "reminder_sent_today", "reminder_campaign_started_at",
        "last_deadline_reminder_variant", "last_deadline_reminder_sent_at", "reminder_campaign_sends_done",
    ])
    return result
