from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class PaystackTransaction(models.Model):
    """Generic payment record — used by both cohort enrollments and
    marketplace orders so the webhook/seat-hold-cleanup logic only has to
    be written once."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    reference = models.CharField(max_length=100, unique=True)
    amount_kobo = models.PositiveBigIntegerField(help_text="Amount in kobo (Paystack's smallest unit).")
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    paystack_status_raw = models.CharField(max_length=50, blank=True)
    subaccount_code = models.CharField(
        max_length=100, blank=True, help_text="Set for marketplace orders using Transaction Splits."
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["content_type", "object_id"])]

    def __str__(self):
        return f"{self.reference} ({self.status})"
