from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "j-#y9^jy9+2l1rf_co)zx95jzmb)_m@tc@gqf&0=mp)i@5hd3x"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES["default"]["PASSWORD"] = "hanusovedni"

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

WAGTAILADMIN_BASE_URL = "https://hanusovedni.local"
CSRF_TRUSTED_ORIGINS = ["https://hanusovedni.local"]


def show_toolbar(request):
    return False


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

CSP_REPORT_ONLY = True

try:
    from .local import *
except ImportError:
    pass
