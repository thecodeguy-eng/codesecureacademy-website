import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.payments import services as payment_services
from apps.payments.models import PaystackTransaction

from .forms import CourseForm, CourseModuleForm, TutorApplicationForm
from .models import Course, CourseModule, Payout, Purchase, Tutor


def course_list(request):
    courses = Course.objects.filter(status=Course.Status.ACTIVE).select_related("tutor")
    return render(request, "courses/course_list.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, status=Course.Status.ACTIVE)
    owned = course.is_purchased_by(request.user)
    return render(request, "courses/course_detail.html", {"course": course, "owned": owned})


@login_required
def apply_tutor(request):
    if hasattr(request.user, "tutor_profile"):
        messages.info(request, "You've already applied to teach on Code Secure Academy.")
        return redirect("courses:tutor_dashboard")

    if request.method == "POST":
        form = TutorApplicationForm(request.POST)
        if form.is_valid():
            tutor = form.save(commit=False)
            tutor.user = request.user
            tutor.save()
            messages.success(request, "Application received — we'll review it shortly.")
            return redirect("courses:tutor_dashboard")
    else:
        form = TutorApplicationForm()

    return render(request, "courses/apply_tutor.html", {"form": form})


@login_required
def tutor_dashboard(request):
    tutor = get_object_or_404(Tutor, user=request.user)
    courses = tutor.courses.all()
    payouts = tutor.payouts.select_related("purchase__course").all()
    totals = payouts.aggregate(
        paid=Sum("amount_naira", filter=Q(status=Payout.Status.PAID)),
        pending=Sum("amount_naira", filter=Q(status=Payout.Status.PENDING)),
    )
    return render(
        request,
        "courses/tutor_dashboard.html",
        {
            "tutor": tutor,
            "courses": courses,
            "payouts": payouts[:20],
            "total_paid": totals["paid"] or 0,
            "total_pending": totals["pending"] or 0,
        },
    )


@login_required
def create_course(request):
    tutor = get_object_or_404(Tutor, user=request.user, status=Tutor.Status.APPROVED)

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.tutor = tutor
            course.save()
            messages.success(request, "Course submitted — it'll go live once approved. Now add your modules.")
            return redirect("courses:add_module", slug=course.slug)
    else:
        form = CourseForm()

    return render(request, "courses/course_form.html", {"form": form})


@login_required
def add_module(request, slug):
    tutor = get_object_or_404(Tutor, user=request.user, status=Tutor.Status.APPROVED)
    course = get_object_or_404(Course, slug=slug, tutor=tutor)

    if request.method == "POST":
        form = CourseModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, "Module added.")
            return redirect("courses:tutor_dashboard")
    else:
        form = CourseModuleForm()

    return render(request, "courses/module_form.html", {"form": form, "course": course})


@login_required
def start_checkout(request, slug):
    course = get_object_or_404(Course, slug=slug, status=Course.Status.ACTIVE)

    purchase = Purchase.objects.create(student=request.user, course=course, amount_naira=course.price_naira)

    reference = f"CSA-CRS-{purchase.id}-{uuid.uuid4().hex[:8]}"
    callback_url = request.build_absolute_uri(reverse("payments:verify_callback", args=[reference]))

    # Unlike marketplace checkout, this is NOT split at the gateway — the
    # full amount settles into the platform's own Paystack balance, and the
    # tutor's cut is paid out separately afterward (see courses.models.Payout).
    try:
        data = payment_services.initialize_transaction(
            email=request.user.email,
            amount_naira=course.price_naira,
            reference=reference,
            callback_url=callback_url,
        )
    except payment_services.PaystackError as exc:
        messages.error(request, f"Couldn't start payment: {exc}")
        return redirect("courses:course_detail", slug=slug)

    PaystackTransaction.objects.create(
        reference=reference,
        amount_kobo=int(course.price_naira * 100),
        email=request.user.email,
        content_type=ContentType.objects.get_for_model(Purchase),
        object_id=purchase.id,
    )

    return redirect(data["authorization_url"])


@login_required
def purchase_success(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, student=request.user)
    return render(request, "courses/purchase_success.html", {"purchase": purchase})


def watch_module(request, slug, module_id):
    """The paywall enforcement point: no video URL reaches the response
    unless the module is a free preview or the requesting user has a
    confirmed Purchase — checked server-side, not just hidden in the
    template."""
    course = get_object_or_404(Course, slug=slug, status=Course.Status.ACTIVE)
    module = get_object_or_404(CourseModule, id=module_id, course=course)

    if not module.is_watchable_by(request.user):
        messages.error(request, "Buy this course to watch that module.")
        return redirect(course.get_absolute_url())

    ordered = list(course.modules.all())
    index = ordered.index(module) if module in ordered else -1
    prev_module = ordered[index - 1] if index > 0 else None
    next_module = ordered[index + 1] if 0 <= index < len(ordered) - 1 else None

    return render(
        request,
        "courses/watch_module.html",
        {"course": course, "module": module, "prev_module": prev_module, "next_module": next_module},
    )
