from .base import *

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")

BASE_URL = os.environ["DJANGO_BASE_URL"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES["default"]["PASSWORD"] = os.environ["POSTGRES_PASSWORD"]
