"""Thin wrapper around the Paystack REST API. Kept dependency-free (just
`requests`) since this is the one integration every payment flow in the
project routes through."""

import requests
from django.conf import settings


class PaystackError(Exception):
    pass


def _headers():
    return {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }


def _call(method, path, **kwargs):
    try:
        resp = requests.request(method, f"{settings.PAYSTACK_BASE_URL}{path}", headers=_headers(), timeout=15, **kwargs)
        data = resp.json()
    except (requests.RequestException, ValueError) as exc:
        raise PaystackError(str(exc)) from exc
    if not data.get("status"):
        raise PaystackError(data.get("message", "Paystack request failed"))
    return data["data"]


def initialize_transaction(*, email, amount_naira, reference, callback_url, subaccount_code=None):
    payload = {
        "email": email,
        "amount": int(amount_naira * 100),
        "reference": reference,
        "callback_url": callback_url,
    }
    if subaccount_code:
        payload["subaccount"] = subaccount_code
    return _call("POST", "/transaction/initialize", json=payload)


def verify_transaction(reference):
    return _call("GET", f"/transaction/verify/{reference}")


def create_subaccount(*, business_name, bank_code, account_number, percentage_charge):
    payload = {
        "business_name": business_name,
        "bank_code": bank_code,
        "account_number": account_number,
        "percentage_charge": percentage_charge,
    }
    return _call("POST", "/subaccount", json=payload)


def list_banks():
    return _call("GET", "/bank?country=nigeria&currency=NGN")


def create_transfer_recipient(*, name, account_number, bank_code):
    payload = {
        "type": "nuban",
        "name": name,
        "account_number": account_number,
        "bank_code": bank_code,
        "currency": "NGN",
    }
    return _call("POST", "/transferrecipient", json=payload)


def initiate_transfer(*, amount_naira, recipient_code, reason=""):
    """Sends money out of the platform's own Paystack balance to a tutor's
    registered bank account. NOTE: depending on the platform's Paystack
    business verification/settings, a transfer may come back as pending and
    require OTP finalization rather than completing directly via this call —
    confirm this against a real test transaction before relying on it with
    real money, same caution as `create_subaccount`'s docstring above."""
    payload = {
        "source": "balance",
        "amount": int(amount_naira * 100),
        "recipient": recipient_code,
        "reason": reason,
    }
    return _call("POST", "/transfer", json=payload)
