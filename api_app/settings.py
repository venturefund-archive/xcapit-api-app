"""
Django settings for api_app project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG")))
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_prometheus',
    'users.apps.UsersConfig',
    'stats.apps.StatsConfig',
    'profiles.apps.ProfilesConfig',
    'referrals.apps.ReferralsConfig',
    'terms_and_conditions.apps.TermsAndConditionsConfig',
    'administration.apps.AdministrationConfig',
    'subscription_plans.apps.SubscriptionPlansConfig',
    'wallets.apps.WalletsConfig',
    'surveys.apps.SurveysConfig'
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'api_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': os.environ.get('POSTGRES_USER'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# CUSTOM
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 20,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=36),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
}


EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
AWS_ACCESS_KEY_ID = 'AKIAI7GSX7RJ5HIXY6PQ'
AWS_SECRET_ACCESS_KEY = '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'

EMAIL_VALIDATION_FROM = 'developers@wallcryptostreet.com'
EMAIL_VALIDATION_SUBJECT = 'Título del email'
RESET_PASSWORD_EMAIL_FROM = 'developers@wallcryptostreet.com'
RESET_PASSWORD_EMAIL_SUBJECT = 'Título del email'

PWA_DOMAIN = os.environ.get('PWA_DOMAIN')

REFERRAL_EMAIL_FROM = 'developers@wallcryptostreet.com'
REFERRAL_EMAIL_SUBJECT = 'Título del email'

API_NOTIFICATIONS = os.environ.get('API_NOTIFICATIONS')

PROMETHEUS_EXPORT_MIGRATIONS = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s [%(filename)s]-[%(levelname)s]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')
        },
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')
        },
    },
}

CLIENT_ID_1 = os.environ.get('CLIENT_ID_1')
CLIENT_ID_2 = os.environ.get('CLIENT_ID_2')
CLIENT_ID_3 = os.environ.get('CLIENT_ID_3')

API_MERCADOPAGO = os.environ.get('API_MERCADOPAGO')
MERCADOPAGO_ACCESS_TOKEN = os.environ.get('MERCADOPAGO_ACCESS_TOKEN')
DEFAULT_REQUEST_TIMEOUT = int(os.getenv('DEFAULT_REQUEST_TIMEOUT', '10'))

NEW_CAMPAIGN = os.getenv('NEW_CAMPAIGN')
OLD_CAMPAIGN = os.getenv('OLD_CAMPAIGN')
