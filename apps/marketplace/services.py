from django.core.mail import send_mail
from django.urls import reverse


def notify_seller_approved(seller, request=None):
    setup_path = reverse("marketplace:setup_payment_info")
    setup_url = request.build_absolute_uri(setup_path) if request else setup_path
    send_mail(
        subject="You're approved to sell on CSA Marketplace",
        message=(
            f"Hi {seller.business_name},\n\n"
            f"Your application to sell on CSA Marketplace has been approved.\n\n"
            f"One more step before you can list anything: add the bank account you want "
            f"paid into. Every sale splits automatically at checkout once that's done.\n\n"
            f"Add your payment details: {setup_url}"
        ),
        from_email=None,
        recipient_list=[seller.user.email],
        fail_silently=True,
    )


def notify_order_paid(order):
    send_mail(
        subject=f"Order confirmed: {order.listing.title}",
        message=(
            f"Your payment for '{order.listing.title}' went through.\n\n"
            f"The seller ({order.listing.seller.business_name}) has been notified "
            f"and will reach out to you directly to fulfil it."
        ),
        from_email=None,
        recipient_list=[order.buyer.email],
        fail_silently=True,
    )
    seller_email = order.listing.seller.user.email
    if seller_email:
        send_mail(
            subject=f"New sale: {order.listing.title}",
            message=(
                f"{order.buyer.get_full_name() or order.buyer.username} just bought "
                f"'{order.listing.title}' for ₦{order.amount_naira}.\n\n"
                f"Buyer email: {order.buyer.email}\n"
                f"Reach out to fulfil the order."
            ),
            from_email=None,
            recipient_list=[seller_email],
            fail_silently=True,
        )
