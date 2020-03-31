import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False

WAGTAILAPI_BASE_URL = "https://hanusovedni.online"

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")

BASE_URL = os.environ["DJANGO_BASE_URL"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES["default"]["PASSWORD"] = os.environ["POSTGRES_PASSWORD"]

WAGTAILFRONTENDCACHE = {
    "cloudflare": {
        "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
        "BEARER_TOKEN": os.environ["CLOUDFLARE_BEARER_TOKEN"],
        "ZONEID": os.environ["CLOUDFLARE_ZONEID"],
    },
}

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    environment=os.environ["ENVIRONMENT"],
)
