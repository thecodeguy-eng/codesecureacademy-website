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
