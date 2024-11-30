"""Base settings to build other settings files upon."""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
BASE_DIR = ROOT_DIR

DOT_ENV_PATH = os.environ.get("DOT_ENV_PATH", default=f"{ROOT_DIR}/dotenv/.env")
if DOT_ENV_PATH != "prod":
    load_dotenv(DOT_ENV_PATH)

# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
FILE_INFO_SECRET_KEY = os.environ.get("FILE_INFO_SECRET_KEY")
DEBUG = os.environ.get("DJANGO_DEBUG", default=False)
# Local time zone
TIME_ZONE = "Asia/Taipei"
LANGUAGE_CODE = "en-us"
# from django.utils.translation import gettext_lazy as _
# LANGUAGES = [
#     ('en', _('English')),
#     ('fr-fr', _('French')),
#     ('pt-br', _('Portuguese')),
# ]
SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]
APPEND_SLASH = False
TRALLING_SLASH = True

# DATABASES
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SILENCED_SYSTEM_CHECKS = [
    # Allow index names >30 characters, because we are not using Oracle
    "models.E034",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    },
}

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "django_celery_beat",
    "django_celery_results",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "ninja",
    "ninja_extra",
    "ninja_jwt",
    "corsheaders",
    "feedparser",
    "colorlog",
    "django_otp",
    # "encrypted_model_fields",
]
LOCAL_APPS = [
    "core",
    "chatbot",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#
#
# auth-user-model
AUTH_USER_MODEL = "core.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "token/login/"
LOGOUT_REDIRECT_URL = "admin/"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_otp.middleware.OTPMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "static")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = []
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR / "static/media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.allauth_settings",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
# CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""FutureNest inc.""", "futurenest-inc.@example.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
# Force the `admin` sign in process to go through the `django-allauth` workflow
DJANGO_ADMIN_FORCE_ALLAUTH = os.environ.get("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
if DOT_ENV_PATH == "prod":
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            },
            "uvicorn": {
                "format": "%(levelname)-8s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "CRITICAL",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "uvicorn_console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "uvicorn",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "propagate": True,
            },
            "uvicorn": {
                "handlers": ["uvicorn_console"],
                "propagate": True,
            },
        },
    }
# elif os.name == "posix":
#     LOGGING = {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "verbose": {
#                 "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
#             },
#             "uvicorn": {
#                 "()": "colorlog.ColoredFormatter",
#                 "format": "%(log_color)s%(levelname)-8s%(blue)s - %(asctime)s - %(reset)s%(message)s",
#                 "log_colors": {
#                     "DEBUG": "cyan",
#                     "INFO": "green",
#                     "WARNING": "yellow",
#                     "ERROR": "red",
#                     "CRITICAL": "bold_red",
#                 },
#             },
#             "uvicorn_file": {
#                 "format": "%(levelname)-8s - %(asctime)s - %(message)s",
#             },
#         },
#         "handlers": {
#             "console": {
#                 "level": "CRITICAL",
#                 "class": "logging.StreamHandler",
#                 "formatter": "verbose",
#             },
#             "uvicorn_console": {
#                 "level": "DEBUG",
#                 "class": "logging.StreamHandler",
#                 "formatter": "uvicorn",
#             },
#             "file": {
#                 "level": "DEBUG",
#                 "class": "logging.handlers.TimedRotatingFileHandler",
#                 "filename": f"{ROOT_DIR}/logs/{datetime.now(tz=pytz.timezone('Asia/Taipei')).strftime('%Y-%m-%dT%H:%M:%S%z')}.log",
#                 "formatter": "uvicorn_file",
#             },
#         },
#         "loggers": {
#             "django": {
#                 "handlers": ["console"],
#                 "propagate": True,
#             },
#             "uvicorn": {
#                 "handlers": ["file", "uvicorn_console"],
#                 "propagate": True,
#             },
#         },
#     }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            },
            "uvicorn": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(levelname)-8s%(blue)s - %(asctime)s - %(reset)s%(message)s",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
        },
        "handlers": {
            "console": {
                "level": "CRITICAL",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "uvicorn_console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "uvicorn",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "propagate": True,
            },
            "uvicorn": {
                "handlers": ["uvicorn_console"],
                "propagate": True,
            },
        },
    }

# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = os.environ.get("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_USERNAME_REQUIRED = False
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "core.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
ACCOUNT_FORMS = {"signup": "core.forms.UserSignupForm"}
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "core.adapters.SocialAccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/forms.html
SOCIALACCOUNT_FORMS = {"signup": "core.forms.UserSocialSignupForm"}

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:30000",
]

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS384",
    "SIGNING_KEY": os.environ.get("DJANGO_SECRET_KEY"),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "ninja_jwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("ninja_jwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "ninja_jwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    #
    # For Controller Schemas
    # FOR OBTAIN PAIR
    "TOKEN_OBTAIN_PAIR_INPUT_SCHEMA": "config.schemas.TokenObtainPairInputSchema",
    "TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA": "config.schemas.TokenRefreshInputSchema",
    # FOR SLIDING TOKEN
    "TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA": "ninja_jwt.schema.TokenObtainSlidingInputSchema",
    "TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA": "ninja_jwt.schema.TokenRefreshSlidingInputSchema",
    "TOKEN_BLACKLIST_INPUT_SCHEMA": "ninja_jwt.schema.TokenBlacklistInputSchema",
    "TOKEN_VERIFY_INPUT_SCHEMA": "ninja_jwt.schema.TokenVerifyInputSchema",
}

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "Asia/Taipei"

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"

CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 1 * 60 * 60

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS = False
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")
AWS_REGION = os.environ.get("AWS_REGION")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
