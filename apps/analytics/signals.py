from .services import track


def handle_user_signed_up(request, user, **kwargs):
    from apps.referrals.views import REFERRAL_COOKIE_NAME

    referred = bool(request.COOKIES.get(REFERRAL_COOKIE_NAME))
    track("signup", user=user, referred=referred)
