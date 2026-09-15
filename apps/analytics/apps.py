from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.analytics"

    def ready(self):
        from allauth.account.signals import user_signed_up

        from . import signals

        user_signed_up.connect(signals.handle_user_signed_up)
