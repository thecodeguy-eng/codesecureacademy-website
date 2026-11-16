from .services import send_welcome_note


def handle_user_signed_up(request, user, **kwargs):
    send_welcome_note(user)
