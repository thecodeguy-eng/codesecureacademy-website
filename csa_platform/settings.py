"""
Django settings for csa_platform project (Code Secure Academy).
"""

from pathlib import Path

import dj_database_url
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Core / security
# --------------------------------------------------------------------------

SECRET_KEY = config("SECRET_KEY", default="django-insecure-dev-only-change-me")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="https://codesecureacademy.com,https://www.codesecureacademy.com",
    cast=Csv(),
)

SITE_ID = 1

# --------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    # Media storage
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "cloudinary",
    # Auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # CSA apps
    "apps.accounts",
    "apps.core",
    "apps.cohorts",
    "apps.payments",
    "apps.whatsapp",
    "apps.reviews",
    "apps.marketplace",
    "apps.lessons",
    "apps.tutorials",
    "apps.courses",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "csa_platform.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "csa_platform.wsgi.application"

# --------------------------------------------------------------------------
# Database (Supabase Postgres in prod, sqlite for local dev if no URL set)
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=config("DB_SSL_REQUIRE", default=True, cast=bool),
    )
}



# --------------------------------------------------------------------------
# Auth
# --------------------------------------------------------------------------

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "home"

# django-allauth configuration: email verification required, email as the login identifier
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_RATE_LIMITS = {
    "login_failed": "5/300s",
}
ACCOUNT_FORMS = {"signup": "apps.accounts.forms.CSASignupForm"}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("GOOGLE_OAUTH_CLIENT_ID", default=""),
            "secret": config("GOOGLE_OAUTH_CLIENT_SECRET", default=""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
    }
}

# --------------------------------------------------------------------------
# Internationalization
# --------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# Static & media (Cloudinary for uploads, WhiteNoise for static assets)
# --------------------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME", default=""),
    "API_KEY": config("CLOUDINARY_API_KEY", default=""),
    "API_SECRET": config("CLOUDINARY_API_SECRET", default=""),
}

MEDIA_URL = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------
# Email (used for verification links + payment/WhatsApp notifications)
# --------------------------------------------------------------------------

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp-relay.brevo.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="Code Secure Academy <no-reply@codesecureacademy.com>")

# --------------------------------------------------------------------------
# Paystack
# --------------------------------------------------------------------------

PAYSTACK_PUBLIC_KEY = config("PAYSTACK_PUBLIC_KEY", default="pk_test_placeholder")
PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY", default="sk_test_placeholder")
PAYSTACK_BASE_URL = "https://api.paystack.co"

# Minutes a seat/order stays "held" while payment is in flight before cleanup considers it expired
SEAT_HOLD_MINUTES = config("SEAT_HOLD_MINUTES", default=5, cast=int)
# Extra minutes granted if Paystack reports the transaction as still "pending" (e.g. a bank transfer) at expiry
SEAT_HOLD_GRACE_MINUTES = config("SEAT_HOLD_GRACE_MINUTES", default=3, cast=int)
# Shared-secret token required to call /internal/release-expired-holds/ (hit by the external cron pinger)
INTERNAL_TASK_TOKEN = config("INTERNAL_TASK_TOKEN", default="dev-only-change-me")

# Marketplace commission split
MARKETPLACE_CSA_SPLIT_PERCENT = config("MARKETPLACE_CSA_SPLIT_PERCENT", default=10, cast=int)

# Course sales: percent of the sale a tutor is paid out (the rest is CSA's cut). Kept
# separate from MARKETPLACE_CSA_SPLIT_PERCENT so the two can be tuned independently.
COURSE_TUTOR_PAYOUT_PERCENT = config("COURSE_TUTOR_PAYOUT_PERCENT", default=90, cast=int)
# Hours a Payout sits as "pending" before the automatic sweep (release_pending_payouts,
# hit by the same external cron pinger as release_expired_holds) will release it — a short
# safety window to catch a refund/dispute before money actually leaves the platform.
PAYOUT_HOLD_HOURS = config("PAYOUT_HOLD_HOURS", default=48, cast=int)

# --------------------------------------------------------------------------
# Social links (used in templates)
# --------------------------------------------------------------------------

INSTAGRAM_URL = config("INSTAGRAM_URL", default="https://instagram.com/codesecureacademy")
FACEBOOK_URL = config("FACEBOOK_URL", default="https://facebook.com/codesecureacademy")
WHATSAPP_CONTACT_NUMBER = config("WHATSAPP_CONTACT_NUMBER", default="2340000000000")

if not DEBUG:
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
