import os

from corsheaders.defaults import default_headers
from corsheaders.defaults import default_methods

from .base import *  # noqa: F403


ALLOWED_HOSTS = str(os.environ.get("DJANGO_ALLOWED_HOSTS")).split(" ")
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_METHODS = [
    *list(default_methods),
]
CORS_ALLOWED_HEADERS = [
    *list(default_headers),
]
CSRF_TRUSTED_ORIGINS = [
    "https://genihelper-pveec-backend.ainsight.chat",
]

# CACHES
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

# EMAIL
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = os.environ.get("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
if DEBUG:  # noqa: F405
    INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# django-extensions
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]

# Your stuff...
