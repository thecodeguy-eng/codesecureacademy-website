from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.text import slugify

from .models import AnalyticsEvent


@staff_member_required
def insights(request):
    from apps.core.models import ReminderQueueItem, SiteSettings
    from apps.core.services import brevo_account_status
    from apps.referrals.models import ReferralCommission

    since = timezone.now() - timezone.timedelta(days=30)

    signups_by_day = list(
        AnalyticsEvent.objects.filter(name="signup", created_at__gte=since)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
    max_signups_in_a_day = max((row["count"] for row in signups_by_day), default=0)

    def event_count(name, **filters):
        return AnalyticsEvent.objects.filter(name=name, **filters).count()

    enrollment_started = event_count("enrollment_started", created_at__gte=since)
    enrollment_confirmed = event_count("enrollment_confirmed", created_at__gte=since)
    conversion_rate = round(enrollment_confirmed / enrollment_started * 100, 1) if enrollment_started else None

    referral_clicks = event_count("referral_click", created_at__gte=since)
    referral_signups = event_count("signup", created_at__gte=since, metadata__referred=True)

    commission_totals = ReferralCommission.objects.aggregate(
        pending=Sum("commission_amount_naira", filter=Q(status="pending")),
        approved=Sum("commission_amount_naira", filter=Q(status="approved")),
        paid=Sum("commission_amount_naira", filter=Q(status="paid")),
    )

    order_paid_count = event_count("order_paid", created_at__gte=since)
    waitlist_joined_count = event_count("waitlist_joined", created_at__gte=since)

    site_settings = SiteSettings.load()
    brevo_status = brevo_account_status()

    context = {
        "since_days": 30,
        "signups_by_day": signups_by_day,
        "max_signups_in_a_day": max_signups_in_a_day,
        "total_signups_30d": sum(row["count"] for row in signups_by_day),
        "enrollment_started": enrollment_started,
        "enrollment_confirmed": enrollment_confirmed,
        "conversion_rate": conversion_rate,
        "referral_clicks": referral_clicks,
        "referral_signups": referral_signups,
        "commission_totals": commission_totals,
        "order_paid_count": order_paid_count,
        "waitlist_joined_count": waitlist_joined_count,
        "brevo_status": brevo_status,
        "site_settings": site_settings,
        "reminder_queue_remaining": ReminderQueueItem.objects.count(),
    }
    return render(request, "analytics/insights.html", context)


@staff_member_required
def send_blast_view(request):
    from apps.core.forms import BlastEmailForm
    from apps.core.models import BlastRecipient
    from apps.core.services import send_blast

    if request.method == "POST":
        form = BlastEmailForm(request.POST)
        if form.is_valid():
            blast_key = slugify(form.cleaned_data["campaign_name"])[:100]
            result = send_blast(
                blast_key,
                form.cleaned_data["subject"],
                form.cleaned_data["body"],
                cta_label=form.cleaned_data["cta_label"] or None,
                cta_url=form.cleaned_data["cta_url"] or None,
                audience=form.cleaned_data["audience"],
                batch_size=form.cleaned_data["limit"],
            )
            if result["sent"] or result["failed"]:
                messages.success(
                    request,
                    f"Sent {result['sent']} (failed: {result['failed']}). "
                    f"{result['remaining']} left for \"{form.cleaned_data['campaign_name']}\" — "
                    f"come back and send again with the same campaign name to reach them." if result["remaining"]
                    else f"Sent {result['sent']} (failed: {result['failed']}). That was everyone — campaign complete.",
                )
            else:
                messages.info(request, f"Nothing to send — everyone in this audience already has \"{form.cleaned_data['campaign_name']}\".")
            return redirect("analytics:send_blast")
    else:
        form = BlastEmailForm()

    recent_campaigns = (
        BlastRecipient.objects.values("blast_key")
        .annotate(
            total=Count("id"),
            sent=Count("id", filter=Q(sent_at__isnull=False, failed=False)),
            failed=Count("id", filter=Q(failed=True)),
            remaining=Count("id", filter=Q(sent_at__isnull=True)),
        )
        .order_by("blast_key")
    )

    return render(request, "analytics/send_blast.html", {"form": form, "recent_campaigns": recent_campaigns})
