from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Tutor(models.Model):
    """Mirrors `marketplace.Seller`'s pending/approved/rejected workflow and
    admin-only approval — but unlike `Seller`, course sales are NOT split at
    the Paystack gateway. A sale settles fully into the platform's own
    Paystack balance, and the tutor is paid out separately via a `Payout`
    (see below) — see that model for why. `paystack_recipient_code` is a
    Paystack *Transfer Recipient* id (created lazily on first payout), not a
    Subaccount id, so approval itself makes no Paystack call at all."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tutor_profile")
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    bank_code = models.CharField(max_length=10, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    paystack_recipient_code = models.CharField(max_length=100, blank=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    def approve(self):
        self.status = self.Status.APPROVED
        self.approved_at = timezone.now()
        self.save()

    def ensure_paystack_recipient(self):
        """Lazily creates the Paystack Transfer Recipient the first time it's
        actually needed (at payout time), rather than at approval — no point
        calling Paystack for a tutor who never makes a sale."""
        if self.paystack_recipient_code:
            return self.paystack_recipient_code

        from apps.payments import services as payment_services

        data = payment_services.create_transfer_recipient(
            name=self.full_name,
            account_number=self.account_number,
            bank_code=self.bank_code,
        )
        self.paystack_recipient_code = data["recipient_code"]
        self.save(update_fields=["paystack_recipient_code"])
        return self.paystack_recipient_code


class Course(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        ACTIVE = "active", "Active"
        REJECTED = "rejected", "Rejected"

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price_naira = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to="courses/", blank=True, null=True)
    related_subject = models.ForeignKey(
        "tutorials.Subject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        help_text="Lets the matching free tutorial page upsell this course.",
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", args=[self.slug])

    def is_purchased_by(self, user):
        if not user.is_authenticated:
            return False
        return self.purchases.filter(student=user, status=Purchase.Status.PAID).exists()

    @property
    def approved_reviews(self):
        from django.contrib.contenttypes.models import ContentType

        from apps.reviews.models import Review

        purchase_ct = ContentType.objects.get_for_model(Purchase)
        purchase_ids = self.purchases.values_list("id", flat=True)
        return Review.objects.filter(content_type=purchase_ct, object_id__in=purchase_ids, status=Review.Status.APPROVED)

    @property
    def average_rating(self):
        from django.db.models import Avg

        return self.approved_reviews.aggregate(avg=Avg("rating"))["avg"]


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(
        help_text="YouTube (unlisted) link, Google Drive share link, or a Cloudinary-hosted video URL."
    )
    is_preview = models.BooleanField(
        default=False, help_text="Free teaser module — watchable without buying the course."
    )

    class Meta:
        ordering = ["course", "order"]

    def __str__(self):
        return f"{self.course.title}: {self.title}"

    @property
    def is_embeddable_video(self):
        from apps.core.video import is_embeddable_video

        return is_embeddable_video(self.video_url)

    @property
    def embed_video_url(self):
        from apps.core.video import embed_video_url

        return embed_video_url(self.video_url)

    def is_watchable_by(self, user):
        return self.is_preview or self.course.is_purchased_by(user)


class Purchase(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Payment pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_purchases")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="purchases")
    amount_naira = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} -> {self.course} ({self.status})"

    def get_success_url(self):
        return reverse("courses:purchase_success", args=[self.id])

    def mark_confirmed(self):
        if self.status == self.Status.PAID:
            return
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "paid_at"])

        payout_amount = (self.amount_naira * Decimal(settings.COURSE_TUTOR_PAYOUT_PERCENT) / Decimal(100)).quantize(
            Decimal("0.01")
        )
        Payout.objects.get_or_create(
            purchase=self, defaults={"tutor": self.course.tutor, "amount_naira": payout_amount}
        )


class Payout(models.Model):
    """The tutor's share of one sale. Created `pending` the moment the
    matching `Purchase` is confirmed — money is already sitting in the
    platform's own Paystack balance at that point, not the tutor's. Released
    (an actual Paystack Transfer) either by the automatic sweep in
    `apps.payments.views.release_pending_payouts` once it's sat for
    `settings.PAYOUT_HOLD_HOURS`, or immediately via the admin "release now"
    action for urgent one-offs. See `Purchase.mark_confirmed` for creation
    and `csa_platform.settings.PAYOUT_HOLD_HOURS` for why there's a delay at
    all instead of paying out instantly."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="payouts")
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name="payout")
    amount_naira = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    paystack_transfer_code = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tutor} <- {self.purchase} (₦{self.amount_naira}, {self.status})"

    def release(self):
        """NOTE: sending a live transfer requires the platform's own Paystack
        business to be transfer-enabled, and depending on its account
        settings Paystack may require OTP finalization rather than
        completing the transfer directly via this call — confirm against a
        real test transaction before trusting this with real money, same
        caution as `Tutor.approve`'s old subaccount code carried."""
        if self.status == self.Status.PAID:
            return
        from apps.payments import services as payment_services

        try:
            recipient_code = self.tutor.ensure_paystack_recipient()
            data = payment_services.initiate_transfer(
                amount_naira=self.amount_naira,
                recipient_code=recipient_code,
                reason=f"Payout for {self.purchase.course.title}",
            )
            self.paystack_transfer_code = data.get("transfer_code", "")
            self.status = self.Status.PAID
            self.paid_at = timezone.now()
            self.save(update_fields=["paystack_transfer_code", "status", "paid_at"])
        except payment_services.PaystackError:
            self.status = self.Status.FAILED
            self.save(update_fields=["status"])
