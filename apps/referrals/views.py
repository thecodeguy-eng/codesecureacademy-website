from django.core import signing
from django.shortcuts import get_object_or_404, redirect, render

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

    from apps.analytics.services import track

    track("referral_click", partner_id=partner.id, partner_name=partner.name)

    response = redirect("home")
    response.set_cookie(
        REFERRAL_COOKIE_NAME, partner.referral_code,
        max_age=REFERRAL_COOKIE_MAX_AGE, httponly=True, samesite="Lax",
    )
    return response


def partner_dashboard(request, code):
    """Read-only, self-serve stats for a partner — reached only via the
    signed link on Partner.dashboard_url (see that property), not a login.
    Same verify-then-404 pattern as apps.core.views.unsubscribe."""
    partner = get_object_or_404(Partner, referral_code=code)
    token = request.GET.get("t", "")
    try:
        verified_code = signing.loads(token, salt="partner-dashboard", max_age=60 * 60 * 24 * 365)
    except signing.BadSignature:
        return render(request, "referrals/partner_dashboard.html", {"invalid": True})
    if verified_code != code:
        return render(request, "referrals/partner_dashboard.html", {"invalid": True})

    from django.db.models import Q, Sum

    commissions = partner.commissions.order_by("-created_at")
    totals = commissions.aggregate(
        pending=Sum("commission_amount_naira", filter=Q(status="pending")),
        approved=Sum("commission_amount_naira", filter=Q(status="approved")),
        paid=Sum("commission_amount_naira", filter=Q(status="paid")),
    )
    referred_count = partner.referred_users.count()

    return render(
        request,
        "referrals/partner_dashboard.html",
        {
            "partner": partner,
            "referred_count": referred_count,
            "commissions": commissions[:50],
            "totals": totals,
        },
    )
