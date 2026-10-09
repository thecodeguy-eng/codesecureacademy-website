from django.contrib.auth.decorators import login_required
from django.http import Http404
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


def _partner_dashboard_context(partner):
    from django.db.models import Q, Sum

    from apps.cohorts.models import Enrollment
    from apps.marketplace.models import Order

    commissions = partner.commissions.order_by("-created_at")
    totals = commissions.aggregate(
        pending=Sum("commission_amount_naira", filter=Q(status="pending")),
        approved=Sum("commission_amount_naira", filter=Q(status="approved")),
        paid=Sum("commission_amount_naira", filter=Q(status="paid")),
    )
    referrals = list(partner.referred_users.select_related("user").order_by("-created_at"))
    referred_count = len(referrals)

    # Converted = has gone on to actually enroll/buy, not just signed up —
    # this is what makes the referral list "progress" and not just a count.
    converted_ids = set(
        Enrollment.objects.filter(
            student__referral_attribution__partner=partner,
            status=Enrollment.Status.CONFIRMED,
        ).values_list("student_id", flat=True)
    ) | set(
        Order.objects.filter(
            buyer__referral_attribution__partner=partner,
            status=Order.Status.PAID,
        ).values_list("buyer_id", flat=True)
    )
    for r in referrals:
        r.converted = r.user_id in converted_ids

    return {
        "partner": partner,
        "referred_count": referred_count,
        "referrals": referrals,
        "commissions": commissions[:50],
        "totals": totals,
    }


@login_required
def partner_dashboard(request):
    """A partner's own stats — reached by logging in with the credentials
    created for them when their Partner record was added in admin (see
    apps.referrals.services.create_partner_login). Anyone without a
    linked Partner just gets a 404, same as hitting a page that isn't
    theirs."""
    partner = getattr(request.user, "partner_profile", None)
    if partner is None:
        raise Http404
    return render(request, "referrals/partner_dashboard.html", _partner_dashboard_context(partner))
