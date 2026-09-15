import logging

logger = logging.getLogger(__name__)


def track(name, user=None, **metadata):
    """Best-effort event log — never raises. A broken analytics write must
    never break the signup, payment, or click it's attached to."""
    try:
        from .models import AnalyticsEvent

        AnalyticsEvent.objects.create(
            name=name,
            user=user if user is not None and user.is_authenticated else None,
            metadata=metadata,
        )
    except Exception:
        logger.warning("Failed to record analytics event %r", name, exc_info=True)
