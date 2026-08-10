from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.cohorts.models import Enrollment, Track
from apps.courses.models import Purchase as CoursePurchase
from apps.marketplace.models import Order


@login_required
def dashboard(request):
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
        },
    )
