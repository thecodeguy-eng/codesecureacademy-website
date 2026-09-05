from decimal import Decimal

from django.contrib.contenttypes.models import ContentType


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
