import logging

from allauth.account.adapter import DefaultAccountAdapter

logger = logging.getLogger(__name__)


class CSAAccountAdapter(DefaultAccountAdapter):
    """allauth's default adapter calls msg.send() with no fail_silently, so
    any SMTP failure (bad credentials, connection refused, timeout) crashes
    the whole request with a 500 — for signup, resend, and password reset
    alike, since they all go through this same send_mail(). A broken email
    provider should degrade to "the email silently didn't go out", never
    to a 500 blocking the user from completing the flow."""

    def send_mail(self, template_prefix, email, context):
        try:
            super().send_mail(template_prefix, email, context)
        except Exception:
            logger.exception("Failed to send account email (template=%s, to=%s)", template_prefix, email)
