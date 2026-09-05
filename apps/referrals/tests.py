import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from apps.cohorts.models import Cohort, Enrollment, Track
from apps.marketplace.models import Listing, Order, Seller

from .models import Partner, ReferralAttribution, ReferralCommission

User = get_user_model()


class ReferralLinkTests(TestCase):
    def test_visiting_link_sets_cookie_and_redirects_home(self):
        partner = Partner.objects.create(name="Sponsor", email="s@example.com", referral_code="sponsor1")
        response = self.client.get(reverse("referral_link", args=["sponsor1"]))
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.client.cookies["csa_ref"].value, "sponsor1")

    def test_inactive_partner_link_404s(self):
        Partner.objects.create(name="Sponsor", email="s@example.com", referral_code="inactive1", is_active=False)
        response = self.client.get(reverse("referral_link", args=["inactive1"]))
        self.assertEqual(response.status_code, 404)

    def test_unknown_code_404s(self):
        response = self.client.get(reverse("referral_link", args=["doesnotexist"]))
        self.assertEqual(response.status_code, 404)

    def test_referral_code_auto_generated_when_blank(self):
        partner = Partner.objects.create(name="Sponsor", email="s@example.com")
        self.assertTrue(partner.referral_code)


class SignupAttributionTests(TestCase):
    """The whole system hinges on this: a referral has to survive from a
    cookie set on a random page visit all the way to an actual signup,
    which could happen minutes or weeks later."""

    def setUp(self):
        self.partner = Partner.objects.create(name="Sponsor", email="s@example.com", referral_code="sponsor2")

    def _signup(self, email):
        return self.client.post(reverse("account_signup"), {
            "first_name": "Test", "last_name": "User", "email": email,
            "phone_number": "08000000000", "track_of_interest": "",
            "password1": "TestPass123x", "password2": "TestPass123x", "agree_to_terms": "on",
        })

    def test_signup_with_referral_cookie_creates_attribution(self):
        self.client.get(reverse("referral_link", args=["sponsor2"]))
        self._signup("attributed@example.com")
        user = User.objects.get(email="attributed@example.com")
        attribution = ReferralAttribution.objects.get(user=user)
        self.assertEqual(attribution.partner, self.partner)

    def test_signup_without_referral_cookie_creates_no_attribution(self):
        self._signup("organic@example.com")
        user = User.objects.get(email="organic@example.com")
        self.assertFalse(ReferralAttribution.objects.filter(user=user).exists())

    def test_inactive_partner_cookie_does_not_attribute(self):
        self.partner.is_active = False
        self.partner.save()
        # Cookie has to be set directly since the link view itself 404s
        # for an inactive partner (a visitor could never get this cookie
        # through the real link) — this covers the case where a partner
        # is deactivated after links are already out in the wild.
        self.client.cookies["csa_ref"] = "sponsor2"
        self._signup("shouldnotcount@example.com")
        user = User.objects.get(email="shouldnotcount@example.com")
        self.assertFalse(ReferralAttribution.objects.filter(user=user).exists())


class CommissionCalculationTests(TestCase):
    """The one thing this absolutely cannot get wrong: the percentage math,
    and never crediting a purchase to someone who wasn't actually the
    referrer."""

    def setUp(self):
        self.partner = Partner.objects.create(
            name="Sponsor", email="s@example.com", referral_code="sponsor3",
            enrollment_commission_percent=Decimal("10.0"),
            marketplace_commission_percent=Decimal("5.0"),
        )
        self.referred_user = User.objects.create_user(username="referred", email="referred@example.com", password="x")
        ReferralAttribution.objects.create(user=self.referred_user, partner=self.partner)
        self.organic_user = User.objects.create_user(username="organic", email="organic2@example.com", password="x")

    def test_enrollment_confirmation_credits_the_referring_partner(self):
        track = Track.objects.create(slug="cybersecurity", name="Cybersecurity")
        cohort = Cohort.objects.create(
            track=track, start_date=timezone.now().date(),
            end_date=timezone.now().date() + datetime.timedelta(days=56),
            price_naira=5000, seat_count=25, status=Cohort.Status.OPEN,
        )
        enrollment = Enrollment.objects.create(student=self.referred_user, cohort=cohort, status=Enrollment.Status.HELD)
        enrollment.mark_confirmed()

        commission = ReferralCommission.objects.get(
            content_type__model="enrollment", object_id=enrollment.id
        )
        self.assertEqual(commission.partner, self.partner)
        self.assertEqual(commission.kind, ReferralCommission.Kind.ENROLLMENT)
        self.assertEqual(commission.commission_amount_naira, Decimal("500.00"))
        self.assertEqual(commission.status, ReferralCommission.Status.PENDING)

    def test_organic_enrollment_creates_no_commission(self):
        track = Track.objects.create(slug="graphic_design", name="Graphic Design")
        cohort = Cohort.objects.create(
            track=track, start_date=timezone.now().date(),
            end_date=timezone.now().date() + datetime.timedelta(days=56),
            price_naira=5000, seat_count=25, status=Cohort.Status.OPEN,
        )
        enrollment = Enrollment.objects.create(student=self.organic_user, cohort=cohort, status=Enrollment.Status.HELD)
        enrollment.mark_confirmed()
        self.assertFalse(
            ReferralCommission.objects.filter(content_type__model="enrollment", object_id=enrollment.id).exists()
        )

    def test_marketplace_order_credits_the_referring_partner_at_its_own_rate(self):
        seller_user = User.objects.create_user(username="seller", email="seller@example.com", password="x")
        seller = Seller.objects.create(user=seller_user, business_name="Biz", category="digital_product", status="approved")
        listing = Listing.objects.create(seller=seller, slug="a-listing", title="A Listing", category="digital_product", description="x", price_naira=2000, status="active")
        order = Order.objects.create(buyer=self.referred_user, listing=listing, amount_naira=2000, status=Order.Status.PENDING)
        order.mark_confirmed()

        commission = ReferralCommission.objects.get(content_type__model="order", object_id=order.id)
        self.assertEqual(commission.kind, ReferralCommission.Kind.MARKETPLACE)
        self.assertEqual(commission.commission_amount_naira, Decimal("100.00"))

    def test_double_confirmation_never_double_credits(self):
        """mark_confirmed is already guarded against re-running, but the
        DB-level unique constraint is the real safety net here — never
        pay a partner twice for the same purchase."""
        track = Track.objects.create(slug="frontend", name="Frontend Development")
        cohort = Cohort.objects.create(
            track=track, start_date=timezone.now().date(),
            end_date=timezone.now().date() + datetime.timedelta(days=56),
            price_naira=5000, seat_count=25, status=Cohort.Status.OPEN,
        )
        enrollment = Enrollment.objects.create(student=self.referred_user, cohort=cohort, status=Enrollment.Status.HELD)
        enrollment.mark_confirmed()
        enrollment.mark_confirmed()  # no-ops via the status guard, but call the service directly too
        from .services import create_commission_for_enrollment
        create_commission_for_enrollment(enrollment)

        count = ReferralCommission.objects.filter(content_type__model="enrollment", object_id=enrollment.id).count()
        self.assertEqual(count, 1)


class MarkPaidTests(TestCase):
    def test_mark_paid_sets_status_and_timestamp_once(self):
        partner = Partner.objects.create(name="Sponsor", email="s@example.com", referral_code="sponsor4")
        user = User.objects.create_user(username="u", email="u@example.com", password="x")
        ReferralAttribution.objects.create(user=user, partner=partner)
        from django.contrib.contenttypes.models import ContentType
        commission = ReferralCommission.objects.create(
            partner=partner, kind=ReferralCommission.Kind.ENROLLMENT,
            content_type=ContentType.objects.get_for_model(partner), object_id=1,
            source_amount_naira=5000, commission_percent=10, commission_amount_naira=500,
        )
        self.assertIsNone(commission.paid_at)
        commission.mark_paid()
        first_paid_at = commission.paid_at
        self.assertEqual(commission.status, ReferralCommission.Status.PAID)
        commission.mark_paid()
        self.assertEqual(commission.paid_at, first_paid_at)
