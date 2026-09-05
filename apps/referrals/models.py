from decimal import Decimal

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class Partner(models.Model):
    """A sponsor with a shareable referral link. Commission rates live per
    partner (not as a global constant) since different sponsors can have
    different deals."""

    name = models.CharField(max_length=150)
    email = models.EmailField(help_text="Where payout confirmations and any admin notices go.")
    referral_code = models.SlugField(
        unique=True, max_length=30, blank=True,
        help_text="What goes in their link (codesecureacademy.com/r/<code>/). Auto-generated if left blank.",
    )
    enrollment_commission_percent = models.DecimalField(
        max_digits=4, decimal_places=1, default=Decimal("10.0"),
        help_text="Percent of the cohort price paid out when someone they referred enrolls.",
    )
    marketplace_commission_percent = models.DecimalField(
        max_digits=4, decimal_places=1, default=Decimal("5.0"),
        help_text="Percent of the order amount paid out when someone they referred buys on the marketplace.",
    )
    is_active = models.BooleanField(default=True, help_text="Turn off to stop crediting new referrals without deleting history.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.referral_code:
            code = get_random_string(8, allowed_chars="abcdefghijkmnpqrstuvwxyz23456789")
            while Partner.objects.filter(referral_code=code).exists():
                code = get_random_string(8, allowed_chars="abcdefghijkmnpqrstuvwxyz23456789")
            self.referral_code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.referral_code})"

    @property
    def referral_url(self):
        return f"{settings.SITE_URL}/r/{self.referral_code}/"


class ReferralAttribution(models.Model):
    """Permanently ties a student to whichever partner's link brought them
    to sign up. Captured once, at signup (see apps.referrals.signals), and
    never overwritten — a cookie alone isn't enough since the referral has
    to survive from a visit to an eventual payment, sometimes weeks later,
    long after any cookie tracking would normally be trusted."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referral_attribution")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="referred_users")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} referred by {self.partner}"


class ReferralCommission(models.Model):
    """One ledger row per commission-earning event. Never auto-paid out —
    an admin reviews and marks it paid once the transfer is actually made,
    real money going to someone outside the company is worth a human
    glance before it leaves, same reasoning as tutor/seller payouts."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        APPROVED = "approved", "Approved, awaiting payout"
        PAID = "paid", "Paid"

    class Kind(models.TextChoices):
        ENROLLMENT = "enrollment", "Cohort enrollment"
        MARKETPLACE = "marketplace", "Marketplace order"

    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="commissions")
    kind = models.CharField(max_length=12, choices=Kind.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    source_amount_naira = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percent = models.DecimalField(max_digits=4, decimal_places=1)
    commission_amount_naira = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # Belt-and-suspenders against double-crediting the same
            # enrollment/order if mark_confirmed ever runs twice for it.
            models.UniqueConstraint(fields=["content_type", "object_id"], name="unique_commission_per_source"),
        ]

    def __str__(self):
        return f"{self.partner} - ₦{self.commission_amount_naira} ({self.status})"

    def mark_paid(self):
        if self.status == self.Status.PAID:
            return
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "paid_at"])
