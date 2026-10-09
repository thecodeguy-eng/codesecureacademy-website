import logging
from decimal import Decimal

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


def attribute_signup(user, referral_code):
    """Called once, right after a new account is created, if a referral
    cookie is present. Never overwrites an existing attribution — the
    first partner to bring someone in is the one who gets credit."""
    from .models import Partner, ReferralAttribution

    if not referral_code or hasattr(user, "referral_attribution"):
        return
    partner = Partner.objects.filter(referral_code=referral_code, is_active=True).first()
    if not partner:
        return
    ReferralAttribution.objects.get_or_create(user=user, defaults={"partner": partner})


def _create_commission(*, student_or_buyer, source_object, kind, source_amount_naira, percent_field):
    from .models import ReferralCommission

    attribution = getattr(student_or_buyer, "referral_attribution", None)
    if not attribution or not attribution.partner.is_active:
        return None

    partner = attribution.partner
    percent = getattr(partner, percent_field)
    amount = (Decimal(source_amount_naira) * percent / Decimal(100)).quantize(Decimal("0.01"))
    content_type = ContentType.objects.get_for_model(source_object)

    commission, _ = ReferralCommission.objects.get_or_create(
        content_type=content_type,
        object_id=source_object.id,
        defaults={
            "partner": partner,
            "kind": kind,
            "source_amount_naira": source_amount_naira,
            "commission_percent": percent,
            "commission_amount_naira": amount,
        },
    )
    return commission


def create_commission_for_enrollment(enrollment):
    from .models import ReferralCommission

    return _create_commission(
        student_or_buyer=enrollment.student,
        source_object=enrollment,
        kind=ReferralCommission.Kind.ENROLLMENT,
        source_amount_naira=enrollment.cohort.price_naira,
        percent_field="enrollment_commission_percent",
    )


def create_commission_for_order(order):
    from .models import ReferralCommission

    return _create_commission(
        student_or_buyer=order.buyer,
        source_object=order,
        kind=ReferralCommission.Kind.MARKETPLACE,
        source_amount_naira=order.amount_naira,
        percent_field="marketplace_commission_percent",
    )


def _unique_username(email):
    from apps.accounts.models import User

    base = email.split("@")[0] or "partner"
    username = base
    suffix = 1
    while User.objects.filter(username=username).exists():
        suffix += 1
        username = f"{base}{suffix}"
    return username


def create_partner_login(partner):
    """Creates the actual login account for a newly added partner — a
    plain username/password, not the old signed-link scheme. Email
    verification is skipped (marked verified outright) since an admin is
    vouching for this address directly, unlike a public signup."""
    from apps.accounts.models import User

    password = get_random_string(12)
    user = User.objects.create_user(
        username=_unique_username(partner.email),
        email=partner.email,
        password=password,
        first_name=partner.name.split()[0] if partner.name else "",
    )
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    partner.user = user
    partner.save(update_fields=["user"])
    return user, password


def reset_partner_login_password(partner):
    """Issues a fresh password for a partner who already has a login —
    e.g. they lost it. Returns the new plaintext password so the admin can
    pass it on; it's never retrievable again after this."""
    password = get_random_string(12)
    partner.user.set_password(password)
    partner.user.save(update_fields=["password"])
    return password


def send_partner_login_email(partner, password, *, is_reset=False):
    """Best-effort — mirrors CSAAccountAdapter's own failure handling, a
    broken mail provider shouldn't block the admin from creating/resetting
    the partner in the first place."""
    login_url = f"{settings.SITE_URL}/accounts/login/"
    subject = (
        "Your Code Secure Academy partner login was reset"
        if is_reset else "Your Code Secure Academy partner dashboard login"
    )
    html_body = render_to_string(
        "emails/partner_login.html",
        {
            "partner": partner,
            "password": password,
            "login_url": login_url,
            "is_reset": is_reset,
        },
    )
    plain_body = (
        f"Hi {partner.name},\n\n"
        f"{'Your partner dashboard password was just reset.' if is_reset else 'Your partner dashboard is ready.'}\n\n"
        f"Login: {login_url}\n"
        f"Email: {partner.email}\n"
        f"Password: {password}\n\n"
        f"Your referral link: {partner.referral_url}\n\n"
        "Code Secure Academy"
    )
    msg = EmailMultiAlternatives(subject, plain_body, to=[partner.email], from_email="info@codesecureacademy.com")
    msg.attach_alternative(html_body, "text/html")
    try:
        msg.send()
    except Exception:
        logger.exception("Failed to send partner login email to %s", partner.email)
