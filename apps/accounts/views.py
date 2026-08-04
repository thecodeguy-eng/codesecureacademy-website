from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.cohorts.models import Enrollment
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
    return render(
        request,
        "accounts/dashboard.html",
        {"enrollments": enrollments, "orders": orders},
    )
