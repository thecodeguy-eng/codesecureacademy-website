from django import forms
from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.utils import timezone

from .models import Review


class AddTestimonialForm(forms.Form):
    rating = forms.ChoiceField(choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(5, 0, -1)])
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label="What they said")


class AddTestimonialAdminMixin:
    """Adds an "Add testimonial for this purchase" action to an Enrollment
    or Order admin — for a real review collected by phone/WhatsApp and
    typed in on a real student's behalf, not a self-submitted one.
    Still tied to a real person and a real completed purchase; just
    transcribed by staff instead of typed by the student themselves.

    Subclasses implement `get_review_reviewer(obj)` to say who the
    reviewer is for that row (e.g. `obj.student` for Enrollment,
    `obj.buyer` for Order) and `get_review_is_complete(obj)` to say
    whether that row is actually eligible (mirrors the same
    confirmed/paid check apps.reviews.views._owns_completed_purchase
    already enforces for self-submitted reviews).
    """

    def get_review_reviewer(self, obj):
        raise NotImplementedError("Set get_review_reviewer() on this ModelAdmin")

    def get_review_is_complete(self, obj):
        raise NotImplementedError("Set get_review_is_complete() on this ModelAdmin")

    @admin.action(description="Add testimonial for this purchase (collected by phone/WhatsApp)")
    def add_testimonial(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Select exactly one row to attach a testimonial to.", level=messages.ERROR)
            return None

        obj = queryset.first()
        if not self.get_review_is_complete(obj):
            self.message_user(request, "That purchase isn't confirmed/paid yet — can't attach a review to it.", level=messages.ERROR)
            return None

        reviewer = self.get_review_reviewer(obj)
        content_type = ContentType.objects.get_for_model(obj)
        already_exists = Review.objects.filter(reviewer=reviewer, content_type=content_type, object_id=obj.pk).exists()
        if already_exists:
            self.message_user(request, f"{reviewer} already has a review for this purchase.", level=messages.ERROR)
            return None

        form = None
        if "apply" in request.POST:
            form = AddTestimonialForm(request.POST)
            if form.is_valid():
                Review.objects.create(
                    reviewer=reviewer,
                    rating=int(form.cleaned_data["rating"]),
                    body=form.cleaned_data["body"],
                    content_type=content_type,
                    object_id=obj.pk,
                    status=Review.Status.APPROVED,
                    moderated_at=timezone.now(),
                )
                self.message_user(request, f"Testimonial added for {reviewer}, live on the site now.")
                return None

        if form is None:
            form = AddTestimonialForm()

        return render(
            request,
            "admin/add_testimonial_form.html",
            {
                "form": form,
                "queryset": queryset,
                "reviewer": reviewer,
                "purchase": obj,
                "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
                "opts": self.model._meta,
                "title": f"Add testimonial for {reviewer}",
            },
        )
