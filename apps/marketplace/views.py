import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.payments import services as payment_services
from apps.payments.models import PaystackTransaction

from .forms import ListingForm, SellerApplicationForm
from .models import Listing, Order, Seller


def listing_list(request):
    listings = Listing.objects.filter(status=Listing.Status.ACTIVE).select_related("seller")
    category = request.GET.get("category")
    if category:
        listings = listings.filter(category=category)
    return render(
        request,
        "marketplace/listing_list.html",
        {"listings": listings, "categories": Seller.Category.choices, "selected_category": category},
    )


def listing_detail(request, slug):
    listing = get_object_or_404(Listing, slug=slug, status=Listing.Status.ACTIVE)
    return render(request, "marketplace/listing_detail.html", {"listing": listing})


@login_required
def apply_seller(request):
    if hasattr(request.user, "seller_profile"):
        messages.info(request, "You've already applied to sell on CSA Marketplace.")
        return redirect("marketplace:seller_dashboard")

    if request.method == "POST":
        form = SellerApplicationForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()
            messages.success(request, "Application received — we'll review it shortly.")
            return redirect("marketplace:seller_dashboard")
    else:
        form = SellerApplicationForm()

    return render(request, "marketplace/apply_seller.html", {"form": form})


@login_required
def seller_dashboard(request):
    """Unlike courses.Payout, there's no separate payout record here — a
    paid Order settled straight into the seller's Paystack subaccount at
    checkout (see Seller.approve / start_checkout below), so "earnings" is
    just the seller's share of paid orders, computed for display."""
    seller = get_object_or_404(Seller, user=request.user)
    listings = seller.listings.all()
    paid_orders = Order.objects.filter(listing__seller=seller, status=Order.Status.PAID).select_related("listing")
    gross = paid_orders.aggregate(total=Sum("amount_naira"))["total"] or 0
    seller_share_percent = Decimal(100 - settings.MARKETPLACE_CSA_SPLIT_PERCENT)
    seller_earnings = (Decimal(gross) * seller_share_percent / Decimal(100)).quantize(Decimal("0.01"))
    return render(
        request,
        "marketplace/seller_dashboard.html",
        {
            "seller": seller,
            "listings": listings,
            "recent_orders": paid_orders.order_by("-paid_at")[:20],
            "seller_earnings": seller_earnings,
            "seller_share_percent": seller_share_percent,
        },
    )


@login_required
def create_listing(request):
    seller = get_object_or_404(Seller, user=request.user, status=Seller.Status.APPROVED)

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = seller
            listing.save()
            messages.success(request, "Listing submitted — it'll go live once approved.")
            return redirect("marketplace:seller_dashboard")
    else:
        form = ListingForm()

    return render(request, "marketplace/listing_form.html", {"form": form})


@login_required
def start_checkout(request, slug):
    listing = get_object_or_404(Listing, slug=slug, status=Listing.Status.ACTIVE)

    order = Order.objects.create(buyer=request.user, listing=listing, amount_naira=listing.price_naira)

    reference = f"CSA-ORD-{order.id}-{uuid.uuid4().hex[:8]}"
    callback_url = request.build_absolute_uri(reverse("payments:verify_callback", args=[reference]))
    subaccount_code = listing.seller.paystack_subaccount_code or None

    try:
        data = payment_services.initialize_transaction(
            email=request.user.email,
            amount_naira=listing.price_naira,
            reference=reference,
            callback_url=callback_url,
            subaccount_code=subaccount_code,
        )
    except payment_services.PaystackError as exc:
        messages.error(request, f"Couldn't start payment: {exc}")
        return redirect("marketplace:listing_detail", slug=slug)

    PaystackTransaction.objects.create(
        reference=reference,
        amount_kobo=int(listing.price_naira * 100),
        email=request.user.email,
        subaccount_code=subaccount_code or "",
        content_type=ContentType.objects.get_for_model(Order),
        object_id=order.id,
    )

    return redirect(data["authorization_url"])


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, "marketplace/order_success.html", {"order": order})
