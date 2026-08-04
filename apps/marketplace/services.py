from django.core.mail import send_mail


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
