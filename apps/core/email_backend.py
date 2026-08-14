"""Sends transactional email via Brevo's HTTPS REST API instead of SMTP.

Render (and cloud hosts generally) can have flaky outbound SMTP — port 587
auth handshakes are a common source of connection/timeout failures that
never show up in local dev. The REST API goes over plain HTTPS (443),
same as every other outbound call this app already makes (Paystack,
Cloudinary), and uses the same Brevo account/sender domain — just a
different, more reliable transport.
"""

from email.utils import parseaddr

import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

API_URL = "https://api.brevo.com/v3/smtp/email"


def _contact(address):
    name, email = parseaddr(address)
    contact = {"email": email}
    if name:
        contact["name"] = name
    return contact


class BrevoAPIEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        sent = 0
        for message in email_messages:
            try:
                self._send_one(message)
                sent += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent

    def _send_one(self, message):
        payload = {
            "sender": _contact(message.from_email or settings.DEFAULT_FROM_EMAIL),
            "to": [_contact(addr) for addr in message.to],
            "subject": message.subject,
            "textContent": message.body,
        }
        if message.cc:
            payload["cc"] = [_contact(addr) for addr in message.cc]
        if message.bcc:
            payload["bcc"] = [_contact(addr) for addr in message.bcc]

        for content, mimetype in getattr(message, "alternatives", []):
            if mimetype == "text/html":
                payload["htmlContent"] = content
                break

        resp = requests.post(
            API_URL,
            json=payload,
            headers={
                "api-key": settings.BREVO_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=15,
        )
        if resp.status_code >= 300:
            raise RuntimeError(f"Brevo API send failed ({resp.status_code}): {resp.text[:300]}")
