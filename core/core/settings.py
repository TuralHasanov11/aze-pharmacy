import os
from pathlib import Path

import dj_database_url
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = str(os.environ.get("DEBUG")) == "True"
SITE_URL = os.environ.get("SITE_URL")
SITE_HOST = os.environ.get("SITE_HOST")

ALLOWED_HOSTS = [SITE_HOST, os.environ.get("SITE_HOST2", None)]

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [SITE_URL, os.environ.get(
        "SITE_URL2", None), os.environ.get("PAYRIFF_DOMAIN"), 
        os.environ.get("PAYRIFF_URL")]
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'django_cleanup.apps.CleanupConfig',
    'ckeditor',
    'ckeditor_uploader',
    'storages',
    'rest_framework',
    'rosetta',
    'bootstrap_datepicker_plus',
    'corsheaders',
    'simple_history',
    'axes',
    "log_viewer",
    'django_crontab',
    'mptt',

    'main',
    'news',
    'services',
    'library',
    'store',
    'user',
    'cart',
    'checkout',
    'orders',
    'wishlist',
    'administration',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'axes.middleware.AxesMiddleware',
    'core.middleware.MaintenanceModeMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_COOLOFF_TIME = 0.25
AXES_FAILURE_LIMIT = 6
AXES_RESET_ON_SUCCESS = True


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.default_menu',
                'main.context_processors.site_info',
                'main.context_processors.default_footer_menu',
                'core.context_processors.config',
                'administration.context_processors.admin_menu',
                'store.context_processors.category_list',
                'cart.context_processors.cart',
                'wishlist.context_processors.wishlist',
            ],
        },
    },
]


ASGI_APPLICATION = 'core.asgi.application'
WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT"),
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL", None)
if DATABASE_URL:
    db_from_env = dj_database_url.config(
        default=DATABASE_URL, conn_max_age=1800)
    DATABASES['default'].update(db_from_env)


if not DEBUG:
    CRONJOBS = [
        ('0 0 * * 0', 'orders.cron.delete_expired_orders')
    ]


AUTH_USER_MODEL = 'user.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = "administration:auth-login"
LOGIN_REDIRECT_URL = "administration:index"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('az', _('Azerbaijani')),
    ('en', _('English')),
    ('ru', _('Russian')),
)

LANGUAGE_CODE = 'az'


LOCALE_PATHS = (
    BASE_DIR / 'locale/',
)


LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = '/info.log'
LOG_PATH = f"{LOG_DIR}/{LOG_FILE}"
CRON_LOG_FILE = '/cron.log'
CRON_LOG_PATH = f"{LOG_DIR}/{CRON_LOG_FILE}"

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

if not os.path.exists(LOG_PATH):
    f = open(LOG_PATH, 'w').close()
else:
    f = open(LOG_PATH, "a").close()


if not os.path.exists(CRON_LOG_PATH):
    f = open(CRON_LOG_PATH, 'w').close()
else:
    f = open(CRON_LOG_PATH, "a").close()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        'main': {
            'format': '{levelname} at {asctime} in {module} - {name} - {message}',
            'style': '{'
        },
        'cron': {
            'format': '{levelname} at {asctime} in {module} - {name} - {message}',
            'style': '{'
        }
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "main",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            'formatter': 'main',
        },
        'file': {
            'level': 'WARNING',
            'formatter': 'main',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH,
        },
        'cron': {
            'level': 'INFO',
            'formatter': 'cron',
            'class': 'logging.FileHandler',
            'filename': CRON_LOG_PATH,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "main": {
            "handlers": ["file", "console"],
            "propagate": True,
            "level": "WARNING",
        },
        "cron": {
            "handlers": ["cron", "console"],
            "propagate": True,
            "level": "INFO",
        }
    },
}

MESSAGE_TAGS = {
    messages.constants.DEBUG: 'alert-secondary',
    messages.constants.INFO: 'alert-info',
    messages.constants.SUCCESS: 'alert-success',
    messages.constants.WARNING: 'alert-warning',
    messages.constants.ERROR: 'alert-danger',
}

USE_S3 = str(os.environ.get("USE_S3")) == "True"

if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)
    AWS_S3_FILE_OVERWRITE = str(os.environ.get(
        "AWS_S3_FILE_OVERWRITE")) == "True"
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_QUERYSTRING_AUTH = False
    DEFAULT_FILE_STORAGE = 'core.storages.MediaStore'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/home/vetagroa/public_html/media/'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_cdn'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_IMAGE_BACKEND = "ckeditor_uploader.backends.PillowBackend"
CKEDITOR_UPLOAD_PATH = "uploads/"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "")
EMAIL_USE_TLS = str(os.environ.get("EMAIL_USE_TLS")) == "True"
EMAIL_USE_LOCALTIME = True

CKEDITOR_CONFIGS = {
    'default': {
        'height': 900,
    },
}


TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)
TWILIO_PHONE = os.environ.get('TWILIO_PHONE', None)
TWILIO_WHATSAPP = os.environ.get('TWILIO_WHATSAPP', None)


PAYRIFF_SECRET_KEY = os.environ.get('PAYRIFF_SECRET_KEY', None)
PAYRIFF_API_ENDPOINT = os.environ.get('PAYRIFF_API_ENDPOINT', None)
PAYRIFF_MERCHANT = os.environ.get('PAYRIFF_MERCHANT', None)


SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True


LOG_VIEWER_FILES = ['info']
LOG_VIEWER_FILES_PATTERN = '*.log*'
LOG_VIEWER_FILES_DIR = 'logs/'
LOG_VIEWER_PAGE_LENGTH = 25
LOG_VIEWER_MAX_READ_LINES = 1000
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25
LOG_VIEWER_PATTERNS = ['[INFO]', '[DEBUG]',
                       '[WARNING]', '[ERROR]', '[CRITICAL]']
LOG_VIEWER_EXCLUDE_TEXT_PATTERN = None


MAINTENANCE_MODE = int(os.environ.get("MAINTENANCE_MODE", 0))
MAINTENANCE_BYPASS_QUERY = os.environ.get("MAINTENANCE_BYPASS_QUERY")

PUSHER_APP_ID = os.environ.get("PUSHER_APP_ID")
PUSHER_APP_KEY = os.environ.get("PUSHER_APP_KEY")
PUSHER_APP_SECRET = os.environ.get("PUSHER_APP_SECRET")
PUSHER_APP_CLUSTER = os.environ.get("PUSHER_APP_CLUSTER")
PUSHER_SSL = str(os.environ.get("PUSHER_SSL")) == "True"
