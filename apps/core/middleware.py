import logging
import random
import threading

logger = logging.getLogger(__name__)

NUDGE_PROBABILITY = 0.005  # roughly 1 in 200 requests


class ReminderCampaignFallbackMiddleware:
    """The reminder campaign is meant to advance via an external cron
    service hitting a dedicated endpoint every ~2 minutes (see
    apps.payments.views.release_expired_holds) — but that pinger lives
    outside this codebase entirely, and has already gone silent once for
    14+ hours with nothing on our end able to see or alert on it. As a
    redundant trigger, a small fraction of ordinary site requests also
    nudge the campaign along in a background thread, so real visitor
    traffic keeps it moving even if the external pinger stops again.

    Fires rarely enough (~1 in 200 requests) to add no meaningful load,
    and does the actual work off-thread so it never slows down the page
    that happened to trigger it. send_deadline_reminder_if_due is already
    idempotent and self-throttled, so overlapping with the external
    pinger just means an extra harmless "not due yet" check sometimes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if random.random() < NUDGE_PROBABILITY:
            threading.Thread(target=self._nudge, daemon=True).start()
        return self.get_response(request)

    @staticmethod
    def _nudge():
        try:
            from apps.core.services import send_deadline_reminder_if_due

            send_deadline_reminder_if_due()
        except Exception:
            logger.exception("Reminder campaign fallback nudge failed")
