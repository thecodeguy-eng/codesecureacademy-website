from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Review
from .services import notify_admin_of_general_review


def testimonials(request):
    """Every real, approved review in one place — never seeded with
    placeholder content. Renders an honest empty state until real
    students actually leave one."""
    reviews = Review.objects.filter(status=Review.Status.APPROVED).select_related("reviewer")
    return render(request, "reviews/testimonials.html", {"reviews": reviews})


def _owns_completed_purchase(user, purchase):
    """Only the Enrollment/Order module knows what "completed" means for
    itself, so we ask the object rather than hard-coding per-model rules
    here."""
    owner_field = "student" if hasattr(purchase, "student") else "buyer"
    is_owner = getattr(purchase, owner_field, None) == user
    is_complete = getattr(purchase, "status", None) in ("confirmed", "paid")
    return is_owner and is_complete


@login_required
def submit_review(request, app_label, model_name, object_id):
    content_type = get_object_or_404(ContentType, app_label=app_label, model=model_name)
    model_class = content_type.model_class()
    purchase = get_object_or_404(model_class, id=object_id)

    if not _owns_completed_purchase(request.user, purchase):
        messages.error(request, "You can only review something you've actually bought.")
        return redirect("home")

    existing = Review.objects.filter(reviewer=request.user, content_type=content_type, object_id=object_id).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.content_type = content_type
            review.object_id = object_id
            review.status = Review.Status.PENDING
            review.save()
            messages.success(request, "Thanks! Your review is in the queue for approval.")
            return redirect("dashboard")
    else:
        form = ReviewForm(instance=existing)

    return render(request, "reviews/submit_review.html", {"form": form, "purchase": purchase})


@login_required
def submit_general_review(request):
    """Open to anyone with an account, not just confirmed buyers — the
    CEO wants reviews from people who haven't bought anything yet too.
    These go in the same PENDING queue as purchase-verified reviews, but
    also email the admin so an unverified review doesn't just sit
    unnoticed in the queue the way a purchase-linked one might."""
    existing = Review.objects.filter(reviewer=request.user, content_type__isnull=True).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            is_new = existing is None
            review = form.save(commit=False)
            review.reviewer = request.user
            review.content_type = None
            review.object_id = None
            review.status = Review.Status.PENDING
            review.save()
            if is_new:
                notify_admin_of_general_review(review)
            messages.success(request, "Thanks! Your review is in the queue for approval.")
            return redirect("reviews:testimonials")
    else:
        form = ReviewForm(instance=existing)

    return render(request, "reviews/submit_general_review.html", {"form": form})
