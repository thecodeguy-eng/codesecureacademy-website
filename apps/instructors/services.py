import logging

from allauth.account.models import EmailAddress
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


def _unique_username(email):
    from apps.accounts.models import User

    base = email.split("@")[0] or "tutor"
    username = base
    suffix = 1
    while User.objects.filter(username=username).exists():
        suffix += 1
        username = f"{base}{suffix}"
    return username


def create_instructor_login(instructor):
    """Same pattern as apps.referrals.services.create_partner_login —
    a plain username/password created the moment admin adds the tutor,
    not a self-signup flow. Email verification is skipped outright since
    admin is vouching for the address directly."""
    from apps.accounts.models import User

    password = get_random_string(12)
    user = User.objects.create_user(
        username=_unique_username(instructor.email),
        email=instructor.email,
        password=password,
        first_name=instructor.name.split()[0] if instructor.name else "",
    )
    EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
    instructor.user = user
    instructor.save(update_fields=["user"])
    return user, password


def reset_instructor_login_password(instructor):
    password = get_random_string(12)
    instructor.user.set_password(password)
    instructor.user.save(update_fields=["password"])
    return password


def send_instructor_login_email(instructor, password, *, is_reset=False):
    login_url = f"{settings.SITE_URL}/accounts/login/"
    subject = (
        "Your Code Secure Academy tutor login was reset"
        if is_reset else "Your Code Secure Academy tutor dashboard login"
    )
    html_body = render_to_string(
        "emails/instructor_login.html",
        {"instructor": instructor, "password": password, "login_url": login_url, "is_reset": is_reset},
    )
    plain_body = (
        f"Hi {instructor.name},\n\n"
        f"{'Your tutor dashboard password was just reset.' if is_reset else 'Your tutor dashboard is ready.'}\n\n"
        f"Login: {login_url}\n"
        f"Email: {instructor.email}\n"
        f"Password: {password}\n\n"
        "Code Secure Academy"
    )
    msg = EmailMultiAlternatives(subject, plain_body, to=[instructor.email], from_email="info@codesecureacademy.com")
    msg.attach_alternative(html_body, "text/html")
    try:
        msg.send()
    except Exception:
        logger.exception("Failed to send tutor login email to %s", instructor.email)
