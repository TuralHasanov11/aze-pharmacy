import os
from pathlib import Path

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = str(os.environ.get("DEBUG")) == "True"

if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    ALLOWED_HOSTS = [os.environ.get("SITE_URL"), ]


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
    "mptt",
    'rest_framework',
    'rosetta',
    'channels',

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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

WSGI_APPLICATION = 'core.wsgi.application'

ASGI_APPLICATION = 'core.asgi.application'


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

AUTH_USER_MODEL = 'user.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = "administration:auth-login"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('az', _('Azerbaijani')),
    ('ru', _('Russian')),
    ('en', _('English')),
)

LANGUAGE_CODE = 'az'


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

STATIC_URL = '/static/'

STATIC_ROOT = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_UPLOAD_PATH = "uploads/"


MESSAGE_TAGS = {
    messages.constants.DEBUG: 'alert-secondary',
    messages.constants.INFO: 'alert-info',
    messages.constants.SUCCESS: 'alert-success',
    messages.constants.WARNING: 'alert-warning',
    messages.constants.ERROR: 'alert-danger',
}


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)
AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION', None)
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', None)
AWS_S3_FILE_OVERWRITE = str(os.environ.get("DEBUG")) == "1"
AWS_DEFAULT_ACL = os.environ.get("DEBUG",  None)
AWS_QUERYSTRING_AUTH = False
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "") 
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "") 
EMAIL_PORT = os.environ.get("EMAIL_PORT", "")  
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", True) 


CKEDITOR_CONFIGS = {
    'default': {
        'height': 1000,
    },
}

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)
TWILIO_PHONE = os.environ.get('TWILIO_PHONE', None)
# TWILIO_API_KEY = os.environ.get('TWILIO_API_KEY', None)
# TWILIO_API_SECRET = os.environ.get('TWILIO_API_SECRET', None)
# TWILIO_CHAT_SERVICE_SID = os.environ.get('TWILIO_CHAT_SERVICE_SID', None)