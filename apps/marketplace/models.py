from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone


class Seller(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class Category(models.TextChoices):
        DIGITAL_PRODUCT = "digital_product", "Digital product"
        TECH_SERVICE = "tech_service", "Tech service"
        MERCH = "merch", "CSA merch"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller_profile")
    business_name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=Category.choices)
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    bank_code = models.CharField(max_length=10, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    paystack_subaccount_code = models.CharField(max_length=100, blank=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.business_name

    def approve(self):
        """Creates the Paystack subaccount on approval so checkout can
        auto-split the sale — no manual payouts.

        NOTE: verify `percentage_charge` semantics against Paystack's live
        docs before going live — some Paystack API versions treat it as the
        platform's cut and others as the subaccount's cut. Getting this
        backwards sends CSA's 10% to the seller and vice versa. Confirm
        with a real test transaction before flipping this on with real money.
        """
        if not self.paystack_subaccount_code and self.bank_code and self.account_number:
            from apps.payments import services as payment_services

            data = payment_services.create_subaccount(
                business_name=self.business_name,
                bank_code=self.bank_code,
                account_number=self.account_number,
                percentage_charge=settings.MARKETPLACE_CSA_SPLIT_PERCENT,
            )
            self.paystack_subaccount_code = data["subaccount_code"]
        self.status = self.Status.APPROVED
        self.approved_at = timezone.now()
        self.save()


class Listing(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending review"
        ACTIVE = "active", "Active"
        REJECTED = "rejected", "Rejected"

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Seller.Category.choices)
    description = models.TextField()
    price_naira = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to="marketplace/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("marketplace:listing_detail", args=[self.slug])

    @property
    def approved_reviews(self):
        from apps.reviews.models import Review

        order_ct = ContentType.objects.get_for_model(Order)
        order_ids = self.orders.values_list("id", flat=True)
        return Review.objects.filter(content_type=order_ct, object_id__in=order_ids, status=Review.Status.APPROVED)

    @property
    def average_rating(self):
        return self.approved_reviews.aggregate(avg=Avg("rating"))["avg"]


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Payment pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="marketplace_orders")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="orders")
    amount_naira = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.buyer} -> {self.listing} ({self.status})"

    def get_success_url(self):
        return reverse("marketplace:order_success", args=[self.id])

    def mark_confirmed(self):
        if self.status == self.Status.PAID:
            return
        self.status = self.Status.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "paid_at"])
        from . import services

        services.notify_order_paid(self)
