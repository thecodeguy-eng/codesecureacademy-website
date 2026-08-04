from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    """One review per completed purchase (an Enrollment or a marketplace
    Order) — not one per person total, since a buyer can legitimately
    complete more than one purchase across the academy + marketplace."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    body = models.TextField(max_length=2000)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    purchase = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)
    moderated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["reviewer", "content_type", "object_id"], name="one_review_per_purchase"
            )
        ]

    def __str__(self):
        return f"{self.reviewer} rated {self.rating}/5 ({self.status})"

    @property
    def display_context(self):
        """A short subtitle for review cards — the track+cohort for a
        cohort enrollment, or the listing title for a marketplace order.
        Kept on the model so every template (homepage, per-track pages)
        renders it the same way without re-deriving the logic."""
        obj = self.purchase
        if obj is None:
            return ""
        if hasattr(obj, "cohort"):
            return f"{obj.cohort.track.name} · {obj.cohort.start_date:%b %Y}"
        if hasattr(obj, "listing"):
            return obj.listing.title
        return ""
