from django.shortcuts import get_object_or_404, redirect

from .models import Partner

REFERRAL_COOKIE_NAME = "csa_ref"
REFERRAL_COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days — long enough that a partner's audience can
# see the link, think it over, and still sign up later and have it count.


def referral_link(request, code):
    """A partner's shareable link. Not a landing page of its own, just
    drops a cookie identifying them and sends the visitor on to the
    homepage like normal — attribution happens later, at signup, if the
    cookie is still there (see apps.referrals.signals)."""
    partner = get_object_or_404(Partner, referral_code=code, is_active=True)
    response = redirect("home")
    response.set_cookie(
        REFERRAL_COOKIE_NAME, partner.referral_code,
        max_age=REFERRAL_COOKIE_MAX_AGE, httponly=True, samesite="Lax",
    )
    return response
