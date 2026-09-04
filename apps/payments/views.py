import hashlib
import hmac
import json

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import services
from .models import PaystackTransaction


def _confirm_transaction(txn, paystack_data):
    """Idempotent: safe to call more than once for the same reference,
    since Paystack can deliver the same webhook event multiple times."""
    if txn.status != PaystackTransaction.Status.SUCCESS:
        txn.status = PaystackTransaction.Status.SUCCESS
        txn.paystack_status_raw = paystack_data.get("status", "")
        txn.verified_at = timezone.now()
        txn.save(update_fields=["status", "paystack_status_raw", "verified_at"])

    obj = txn.content_object
    if obj is not None and hasattr(obj, "mark_confirmed"):
        obj.mark_confirmed()


@csrf_exempt
@require_POST
def paystack_webhook(request):
    signature = request.headers.get("x-paystack-signature", "")
    computed = hmac.new(settings.PAYSTACK_SECRET_KEY.encode(), request.body, hashlib.sha512).hexdigest()
    if not signature or not hmac.compare_digest(signature, computed):
        return HttpResponseForbidden("Invalid signature")

    try:
        event = json.loads(request.body)
    except ValueError:
        return HttpResponse(status=400)

    if event.get("event") == "charge.success":
        data = event.get("data", {})
        reference = data.get("reference")
        txn = PaystackTransaction.objects.filter(reference=reference).first()
        if txn:
            _confirm_transaction(txn, data)

    # Always 200 on anything we recognized-but-ignored so Paystack stops retrying.
    return HttpResponse(status=200)


def verify_callback(request, reference):
    """Paystack redirects the browser here after checkout. The webhook is
    the source of truth, but we verify synchronously too in case the
    webhook hasn't landed yet, so the user isn't stuck on a blank page."""
    txn = PaystackTransaction.objects.filter(reference=reference).select_related("content_type").first()
    if not txn:
        return render(request, "payments/not_found.html", status=404)

    if txn.status != PaystackTransaction.Status.SUCCESS:
        try:
            result = services.verify_transaction(reference)
            if result.get("status") == "success":
                _confirm_transaction(txn, result)
        except services.PaystackError:
            pass

    obj = txn.content_object
    if obj is not None and hasattr(obj, "get_success_url"):
        return redirect(obj.get_success_url())
    return render(request, "payments/pending.html", {"transaction": txn})


@csrf_exempt
def release_expired_holds(request):
    """Hit every ~2 min by the external free pinger (cron-job.org/UptimeRobot)
    alongside the keep-alive ping, since Render's free tier has no built-in
    cron worker. Implements the seat-hold grace check: a slow-but-successful
    bank transfer gets a short extra window instead of losing the seat."""
    token = request.headers.get("X-Internal-Token") or request.GET.get("token")
    if not token or token != settings.INTERNAL_TASK_TOKEN:
        return HttpResponseForbidden("Invalid token")

    from apps.cohorts.models import Enrollment

    now = timezone.now()
    hold_cutoff = now - timezone.timedelta(minutes=settings.SEAT_HOLD_MINUTES)
    released, extended, confirmed = 0, 0, 0

    expired = Enrollment.objects.select_related("cohort").filter(
        status=Enrollment.Status.HELD, seat_held_at__lte=hold_cutoff
    )
    enrollment_ct = ContentType.objects.get_for_model(Enrollment)

    for enrollment in expired:
        if enrollment.grace_extended_until and enrollment.grace_extended_until > now:
            continue  # still inside its grace window, leave it alone this pass

        txn = (
            PaystackTransaction.objects.filter(content_type=enrollment_ct, object_id=enrollment.id)
            .order_by("-created_at")
            .first()
        )

        paystack_status = None
        result = None
        if txn:
            try:
                result = services.verify_transaction(txn.reference)
                paystack_status = result.get("status")
            except services.PaystackError:
                paystack_status = None

        if paystack_status == "success" and txn:
            _confirm_transaction(txn, result)
            confirmed += 1
        elif paystack_status == "pending" and not enrollment.grace_extended_until:
            # Bank transfer likely still confirming — give it a short extra window
            # instead of punishing a legitimately-slow-but-successful payment.
            enrollment.grace_extended_until = now + timezone.timedelta(minutes=settings.SEAT_HOLD_GRACE_MINUTES)
            enrollment.save(update_fields=["grace_extended_until"])
            extended += 1
        else:
            enrollment.status = Enrollment.Status.EXPIRED
            enrollment.save(update_fields=["status"])
            enrollment.cohort.refresh_status()
            released += 1

    from apps.core.services import send_deadline_reminder_if_due

    reminder_result = send_deadline_reminder_if_due()

    return JsonResponse(
        {"released": released, "extended": extended, "confirmed": confirmed, "deadline_reminder": reminder_result}
    )


@csrf_exempt
def release_pending_payouts(request):
    """Hit by the same external pinger as `release_expired_holds`, same
    token check. Releases any tutor Payout that's sat `pending` for at
    least `settings.PAYOUT_HOLD_HOURS` — a short safety window between a
    course sale landing in the platform's Paystack balance and the tutor's
    cut actually being transferred out, so an obvious refund/dispute can
    still be caught before money leaves. To hold a specific payout back
    past its window, just don't include it here — an admin can flip its
    status away from `pending` in /admin/ any time before this runs."""
    token = request.headers.get("X-Internal-Token") or request.GET.get("token")
    if not token or token != settings.INTERNAL_TASK_TOKEN:
        return HttpResponseForbidden("Invalid token")

    from apps.courses.models import Payout

    cutoff = timezone.now() - timezone.timedelta(hours=settings.PAYOUT_HOLD_HOURS)
    due = Payout.objects.filter(status=Payout.Status.PENDING, created_at__lte=cutoff)

    released, failed = 0, 0
    for payout in due:
        payout.release()
        if payout.status == Payout.Status.PAID:
            released += 1
        else:
            failed += 1

    return JsonResponse({"released": released, "failed": failed})


def healthz(request):
    """Cheap endpoint for the external keep-alive pinger to hit."""
    return JsonResponse({"status": "ok"})
