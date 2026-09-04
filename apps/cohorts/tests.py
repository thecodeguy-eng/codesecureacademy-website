import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Cohort, Track

User = get_user_model()

TODAY = timezone.now().date()


def make_cohort(track, **overrides):
    defaults = {
        "track": track,
        "start_date": TODAY,
        "end_date": TODAY + datetime.timedelta(days=56),
        "price_naira": 5000,
        "seat_count": 25,
        "status": Cohort.Status.OPEN,
    }
    defaults.update(overrides)
    return Cohort.objects.create(**defaults)


class AcceptingEnrollmentTests(TestCase):
    """accepting_enrollment is the single gate every enroll button and the
    checkout view itself checks — a bug here either wrongly blocks a
    legitimate signup or, worse, lets someone enroll after the deadline
    or into a closed cohort."""

    def setUp(self):
        self.track = Track.objects.create(slug="frontend", name="Frontend Development")

    def test_open_with_seats_and_no_deadline_accepts(self):
        cohort = make_cohort(self.track)
        self.assertTrue(cohort.accepting_enrollment)
        self.assertFalse(cohort.is_past_deadline)

    def test_open_with_future_deadline_accepts(self):
        cohort = make_cohort(self.track, enrollment_deadline=TODAY + datetime.timedelta(days=1))
        self.assertTrue(cohort.accepting_enrollment)

    def test_deadline_today_still_accepts(self):
        """The deadline date itself is still open, it closes the day after."""
        cohort = make_cohort(self.track, enrollment_deadline=TODAY)
        self.assertTrue(cohort.accepting_enrollment)

    def test_past_deadline_blocks_even_with_seats_open(self):
        cohort = make_cohort(self.track, enrollment_deadline=TODAY - datetime.timedelta(days=1))
        self.assertTrue(cohort.is_past_deadline)
        self.assertFalse(cohort.accepting_enrollment)

    def test_closed_status_blocks_regardless_of_deadline(self):
        cohort = make_cohort(
            self.track, status=Cohort.Status.CLOSED, enrollment_deadline=TODAY + datetime.timedelta(days=30)
        )
        self.assertFalse(cohort.accepting_enrollment)

    def test_full_seats_block_regardless_of_deadline(self):
        cohort = make_cohort(
            self.track, seat_count=1, enrollment_deadline=TODAY + datetime.timedelta(days=30)
        )
        student = User.objects.create_user(username="s1", email="s1@example.com", password="x")
        cohort.enrollments.create(student=student, status="confirmed")
        self.assertEqual(cohort.seats_available, 0)
        self.assertFalse(cohort.accepting_enrollment)


class StartCheckoutDeadlineTests(TestCase):
    """The deadline has to be enforced in the view that actually starts a
    payment, not just hidden from the template — otherwise someone who
    still has the enroll URL (bookmarked, or just guessed) could pay after
    the cutoff even though the button never showed."""

    def setUp(self):
        self.track = Track.objects.create(slug="backend", name="Backend Development")
        self.user = User.objects.create_user(username="buyer", email="buyer@example.com", password="x")
        self.client.force_login(self.user)

    def test_checkout_blocked_after_deadline(self):
        cohort = make_cohort(self.track, enrollment_deadline=TODAY - datetime.timedelta(days=1))
        response = self.client.post(
            reverse("cohorts:start_checkout", args=[cohort.id]), follow=True
        )
        self.assertRedirects(response, reverse("cohorts:track_detail", args=[self.track.slug]))
        self.assertFalse(cohort.enrollments.filter(student=self.user).exists())
