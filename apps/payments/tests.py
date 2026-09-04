import hashlib
import hmac
import json

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(PAYSTACK_SECRET_KEY="test-secret-key-for-signature-checks")
class PaystackWebhookSignatureTests(TestCase):
    """The webhook is the one endpoint that turns a "held" seat into a paid,
    confirmed enrollment, and it's publicly reachable with no auth other
    than this signature. If the check ever silently breaks (wrong header
    name, wrong hash, comparison bug), anyone could POST a fake
    charge.success and get free access."""

    def _signed_post(self, body: bytes, secret: str):
        signature = hmac.new(secret.encode(), body, hashlib.sha512).hexdigest()
        return self.client.post(
            reverse("payments:paystack_webhook"),
            data=body,
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE=signature,
        )

    def test_valid_signature_is_accepted(self):
        body = json.dumps({"event": "charge.success", "data": {"reference": "does-not-exist"}}).encode()
        response = self._signed_post(body, settings.PAYSTACK_SECRET_KEY)
        self.assertEqual(response.status_code, 200)

    def test_wrong_secret_is_rejected(self):
        body = json.dumps({"event": "charge.success", "data": {"reference": "does-not-exist"}}).encode()
        response = self._signed_post(body, "not-the-real-secret")
        self.assertEqual(response.status_code, 403)

    def test_missing_signature_header_is_rejected(self):
        body = json.dumps({"event": "charge.success", "data": {}}).encode()
        response = self.client.post(
            reverse("payments:paystack_webhook"), data=body, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_tampered_body_is_rejected(self):
        """Signature computed over the original body must not validate
        against a body that's been modified after signing."""
        original = json.dumps({"event": "charge.success", "data": {"reference": "abc"}}).encode()
        signature = hmac.new(settings.PAYSTACK_SECRET_KEY.encode(), original, hashlib.sha512).hexdigest()
        tampered = json.dumps({"event": "charge.success", "data": {"reference": "xyz"}}).encode()
        response = self.client.post(
            reverse("payments:paystack_webhook"),
            data=tampered,
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE=signature,
        )
        self.assertEqual(response.status_code, 403)
