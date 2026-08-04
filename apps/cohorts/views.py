import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.payments import services
from apps.payments.models import PaystackTransaction
from apps.reviews.models import Review

from .models import Cohort, Enrollment, Track, Waitlist


def track_list(request):
    tracks = Track.objects.filter(is_active=True)
    return render(request, "cohorts/track_list.html", {"tracks": tracks})


def track_detail(request, slug):
    track = get_object_or_404(Track, slug=slug, is_active=True)
    cohort = track.next_cohort
    already_on_waitlist = (
        request.user.is_authenticated
        and Waitlist.objects.filter(student=request.user, track=track).exists()
    )

    enrollment_ct = ContentType.objects.get_for_model(Enrollment)
    track_reviews = (
        Review.objects.filter(
            content_type=enrollment_ct,
            object_id__in=Enrollment.objects.filter(cohort__track=track).values_list("id", flat=True),
            status=Review.Status.APPROVED,
        )
        .select_related("reviewer")
    )

    return render(
        request,
        "cohorts/track_detail.html",
        {
            "track": track,
            "cohort": cohort,
            "already_on_waitlist": already_on_waitlist,
            "track_reviews": track_reviews,
        },
    )


@login_required
def start_checkout(request, cohort_id):
    cohort = get_object_or_404(Cohort, id=cohort_id)
    cohort.refresh_status()

    if cohort.is_full:
        messages.warning(request, "That cohort just filled up — join the waitlist instead.")
        return redirect("cohorts:track_detail", slug=cohort.track.slug)

    existing = Enrollment.objects.filter(
        student=request.user, cohort=cohort, status__in=[Enrollment.Status.HELD, Enrollment.Status.CONFIRMED]
    ).first()
    if existing and existing.status == Enrollment.Status.CONFIRMED:
        messages.info(request, "You're already enrolled in this cohort.")
        return redirect("cohorts:enrollment_success", enrollment_id=existing.id)

    enrollment = existing or Enrollment.objects.create(student=request.user, cohort=cohort)

    reference = f"CSA-ENR-{enrollment.id}-{uuid.uuid4().hex[:8]}"
    callback_url = request.build_absolute_uri(reverse("payments:verify_callback", args=[reference]))

    try:
        data = services.initialize_transaction(
            email=request.user.email,
            amount_naira=cohort.price_naira,
            reference=reference,
            callback_url=callback_url,
        )
    except services.PaystackError as exc:
        messages.error(request, f"Couldn't start payment: {exc}")
        return redirect("cohorts:track_detail", slug=cohort.track.slug)

    PaystackTransaction.objects.create(
        reference=reference,
        amount_kobo=int(cohort.price_naira * 100),
        email=request.user.email,
        content_type=ContentType.objects.get_for_model(Enrollment),
        object_id=enrollment.id,
    )

    return redirect(data["authorization_url"])


@login_required
def enrollment_success(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
    whatsapp_link = None
    if enrollment.status == Enrollment.Status.CONFIRMED:
        from apps.whatsapp.models import TrackWhatsAppGroup

        group = TrackWhatsAppGroup.objects.filter(track=enrollment.cohort.track).first()
        whatsapp_link = group.invite_link if group else None
    return render(
        request,
        "cohorts/enrollment_success.html",
        {"enrollment": enrollment, "whatsapp_link": whatsapp_link},
    )


@login_required
def join_waitlist(request, track_slug):
    track = get_object_or_404(Track, slug=track_slug)
    Waitlist.objects.get_or_create(student=request.user, track=track)
    messages.success(request, "You're on the waitlist — we'll email you the moment a seat opens up.")
    return redirect("cohorts:track_detail", slug=track_slug)
