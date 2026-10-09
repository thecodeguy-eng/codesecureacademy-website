import logging

from django.conf import settings
from django.core.mail import mail_admins

logger = logging.getLogger(__name__)


def notify_admin_of_general_review(review):
    """A review with no purchase behind it is from someone who isn't
    (yet) verified as a real customer — still worth hearing, but it
    needs a human look before it goes public, unlike the purchase-
    verified flow. Best-effort: a broken mail provider shouldn't block
    the reviewer's submission (see CSAAccountAdapter.send_mail for the
    same reasoning elsewhere)."""
    subject = f"New review awaiting approval — {review.reviewer}"
    message = (
        f"{review.reviewer} ({review.reviewer.email}) left a {review.rating}/5 review "
        "with no purchase on file:\n\n"
        f'"{review.body}"\n\n'
        f"Approve or reject it in the admin: {settings.SITE_URL}/admin/reviews/review/{review.id}/change/"
    )
    try:
        mail_admins(subject, message, fail_silently=False)
    except Exception:
        logger.exception("Failed to send admin notification for review %s", review.id)
