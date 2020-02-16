from .base import *

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")

BASE_URL = os.environ["DJANGO_BASE_URL"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES["default"]["PASSWORD"] = os.environ["POSTGRES_PASSWORD"]


STATIC_ROOT = "/static_root"

MEDIA_ROOT = "/media_root"

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://ef973f216d8141d8845ca48d0479eeee@sentry.io/202767",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    # send_default_pii=True
)
