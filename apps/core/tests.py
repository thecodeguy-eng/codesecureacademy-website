import datetime

from django.contrib.auth import get_user_model
from django.core import mail, signing
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.cohorts.models import Cohort, Enrollment, Track

from .models import EmailOptOut, ReminderQueueItem, SiteSettings, WaitlistSignup
from .services import _deadline_reminder_recipients, send_deadline_reminder_if_due, unsubscribe_url

User = get_user_model()


def make_open_cohort(deadline_days_from_now=7):
    track = Track.objects.create(slug="cybersecurity", name="Cybersecurity")
    return Cohort.objects.create(
        track=track,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + datetime.timedelta(days=56),
        enrollment_deadline=timezone.now().date() + datetime.timedelta(days=deadline_days_from_now),
        price_naira=5000,
        seat_count=25,
        status=Cohort.Status.OPEN,
    )


class ReminderRecipientTests(TestCase):
    """The one rule this list absolutely cannot get wrong: someone who's
    already paid must never be on it."""

    def setUp(self):
        self.cohort = make_open_cohort()

    def test_waitlist_and_users_are_both_included(self):
        WaitlistSignup.objects.create(email="lead@example.com")
        User.objects.create_user(username="u1", email="user@example.com", password="x")
        recipients = _deadline_reminder_recipients()
        self.assertIn("lead@example.com", recipients)
        self.assertIn("user@example.com", recipients)

    def test_confirmed_enrollment_is_excluded(self):
        student = User.objects.create_user(username="paid", email="paid@example.com", password="x")
        Enrollment.objects.create(student=student, cohort=self.cohort, status=Enrollment.Status.CONFIRMED)
        recipients = _deadline_reminder_recipients()
        self.assertNotIn("paid@example.com", recipients)

    def test_held_but_unconfirmed_enrollment_is_still_included(self):
        """Someone mid-checkout who hasn't actually paid yet should still
        get reminded — only a CONFIRMED (paid) enrollment exempts them."""
        student = User.objects.create_user(username="held", email="held@example.com", password="x")
        Enrollment.objects.create(student=student, cohort=self.cohort, status=Enrollment.Status.HELD)
        recipients = _deadline_reminder_recipients()
        self.assertIn("held@example.com", recipients)

    def test_unsubscribed_email_is_excluded(self):
        WaitlistSignup.objects.create(email="optout@example.com")
        EmailOptOut.objects.create(email="optout@example.com")
        recipients = _deadline_reminder_recipients()
        self.assertNotIn("optout@example.com", recipients)

    def test_case_insensitive_exclusion(self):
        student = User.objects.create_user(username="caps", email="Paid@Example.com", password="x")
        Enrollment.objects.create(student=student, cohort=self.cohort, status=Enrollment.Status.CONFIRMED)
        WaitlistSignup.objects.create(email="paid@example.com")
        recipients = _deadline_reminder_recipients()
        self.assertNotIn("paid@example.com", recipients)


class ReminderSchedulingTests(TestCase):
    """Covers the actual production bug found and fixed: sending the whole
    list synchronously in one call times out the request it's called from,
    so sends must be queued and drained in chunks, and the self-throttle
    must not re-trigger a second cycle while one is still draining."""

    def setUp(self):
        make_open_cohort()
        WaitlistSignup.objects.create(email="a@example.com")
        WaitlistSignup.objects.create(email="b@example.com")

    def test_no_upcoming_deadline_skips_entirely(self):
        Cohort.objects.all().delete()
        result = send_deadline_reminder_if_due()
        self.assertEqual(result.get("skipped"), "no upcoming deadline")
        self.assertEqual(len(mail.outbox), 0)

    def test_first_call_queues_and_sends_a_chunk(self):
        result = send_deadline_reminder_if_due()
        self.assertGreaterEqual(result.get("sent", 0), 1)
        self.assertEqual(len(mail.outbox), 2)  # both waitlist emails, small enough to fit one chunk

    def test_second_call_same_day_does_not_resend(self):
        send_deadline_reminder_if_due()
        mail.outbox.clear()
        result = send_deadline_reminder_if_due()
        self.assertEqual(result.get("skipped"), "not due yet")
        self.assertEqual(len(mail.outbox), 0)

    def test_leftover_queue_drains_before_checking_if_a_new_cycle_is_due(self):
        """Simulates a cycle that started but didn't finish draining (e.g.
        the request got cut off) — the next call must resume the same
        queue, not evaluate the daily due-check and potentially start a
        second cycle on top of the first."""
        ReminderQueueItem.objects.create(email="leftover@example.com", variant_index=2)
        settings_obj = SiteSettings.load()
        settings_obj.last_deadline_reminder_sent_at = timezone.now() - datetime.timedelta(days=10)
        settings_obj.save()

        result = send_deadline_reminder_if_due()
        self.assertEqual(result.get("variant"), 2)
        self.assertEqual(ReminderQueueItem.objects.count(), 0)


class UnsubscribeTests(TestCase):
    def test_valid_token_opts_out_and_future_sends_exclude_them(self):
        email = "unsub-me@example.com"
        WaitlistSignup.objects.create(email=email)
        token = unsubscribe_url(email).rstrip("/").rsplit("/", 1)[-1]

        response = self.client.get(reverse("unsubscribe", args=[token]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(EmailOptOut.objects.filter(email=email).exists())
        self.assertNotIn(email, _deadline_reminder_recipients())

    def test_garbage_token_does_not_crash_or_opt_anyone_out(self):
        response = self.client.get(reverse("unsubscribe", args=["not-a-real-token"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EmailOptOut.objects.count(), 0)

    def test_token_cannot_be_forged_for_a_different_email(self):
        """Signed with the wrong salt, should be rejected the same as a
        garbage token, not silently accepted as some other email."""
        forged = signing.dumps("victim@example.com", salt="some-other-salt")
        response = self.client.get(reverse("unsubscribe", args=[forged]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(EmailOptOut.objects.filter(email="victim@example.com").exists())
