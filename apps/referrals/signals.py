from .services import attribute_signup
from .views import REFERRAL_COOKIE_NAME


def handle_user_signed_up(request, user, **kwargs):
    code = request.COOKIES.get(REFERRAL_COOKIE_NAME)
    if code:
        attribute_signup(user, code)
