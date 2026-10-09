from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.cohorts.models import Enrollment, Track
from apps.courses.models import Purchase as CoursePurchase
from apps.marketplace.models import Order

from .forms import ResendConfirmationForm


@login_required
def dashboard(request):
    if hasattr(request.user, "partner_profile"):
        return redirect("partner_dashboard")

    enrollments = (
        Enrollment.objects.filter(student=request.user)
        .select_related("cohort", "cohort__track")
        .order_by("-created_at")
    )
    orders = (
        Order.objects.filter(buyer=request.user)
        .select_related("listing")
        .order_by("-created_at")
    )
    course_purchases = (
        CoursePurchase.objects.filter(student=request.user)
        .select_related("course")
        .order_by("-created_at")
    )

    from apps.lessons.models import LessonProgress

    confirmed_track_ids = enrollments.filter(status=Enrollment.Status.CONFIRMED).values_list(
        "cohort__track_id", flat=True
    )
    completed_lesson_ids = set(
        LessonProgress.objects.filter(student=request.user).values_list("lesson_id", flat=True)
    )
    learning_progress = []
    for track in Track.objects.filter(id__in=set(confirmed_track_ids)):
        lessons = list(track.lessons.all())
        if not lessons:
            continue
        done = sum(1 for lesson in lessons if lesson.id in completed_lesson_ids)
        learning_progress.append({
            "track": track, "total": len(lessons), "done": done,
            "percent": round(done / len(lessons) * 100),
        })

    recommended_track = None
    other_tracks = Track.objects.none()
    if not enrollments:
        if request.user.track_of_interest:
            recommended_track = Track.objects.filter(
                slug=request.user.track_of_interest, is_active=True
            ).first()
        if not recommended_track:
            other_tracks = Track.objects.filter(is_active=True)

    return render(
        request,
        "accounts/dashboard.html",
        {
            "enrollments": enrollments,
            "orders": orders,
            "course_purchases": course_purchases,
            "recommended_track": recommended_track,
            "other_tracks": other_tracks,
            "learning_progress": learning_progress,
        },
    )


def resend_confirmation_email(request):
    """Standalone version of allauth's confirmation-email send, reachable
    without being logged in — mandatory email verification otherwise leaves
    a user with a lost/delayed email stuck with no way back in. Doesn't
    reveal whether the address is registered or already verified (same
    message either way), to avoid turning this into an account-enumeration
    endpoint."""
    if request.method == "POST":
        form = ResendConfirmationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            address = EmailAddress.objects.filter(email__iexact=email, verified=False).first()
            if address:
                address.send_confirmation(request)
            messages.success(
                request,
                "If that email is registered and not yet verified, we've just sent a new confirmation link.",
            )
            return redirect("accounts_extra:resend_confirmation")
    else:
        form = ResendConfirmationForm()

    return render(request, "accounts/resend_confirmation.html", {"form": form})
