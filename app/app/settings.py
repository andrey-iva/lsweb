"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8*h^9)x&u3ttu^_k)rxg&_c&n7^n&es)i*^43b*$t-fjiu^hkb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'shop.apps.ShopConfig',
    'django_summernote',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'shop', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'shop.ctx_proc.cart',
                'shop.ctx_proc.currency',
                'shop.ctx_proc.categories',
                'shop.ctx_proc.no_image',
                'shop.ctx_proc.get_services',
                'shop.ctx_proc.get_loop_id',
                'shop.ctx_proc.get_loop_price',
                'shop.ctx_proc.is_install',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# my-app
STATIC_ROOT = 'static/'
MEDIA_ROOT = 'media/'
MEDIA_URL = 'media/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s %(levelname)-1s] START %(message)s END'
        },
        # 'file': {
        #     'format': '%(asctime)s %(name)-1s %(levelname)-1s %(message)s'
        # }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'formatter': 'file',
        #     'filename': 'debug.log'
        # }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console']
            # 'handlers': ['console', 'file']
        }
    }
}

# CORS_ALLOWED_ORIGINS = [
#     'https://suggestions.dadata.ru',
#     'https://api.cdek.ru',
#     'https://api.edu.cdek.ru',
#     'https://www.youtube.com',
#     'https://cdn.jsdelivr.net',
#     'https://maps.api.2gis.ru',
#     'https://i12n.r2r.space',
#     'https://api-maps.yandex.ru',
# ]

CORS_ALLOWED_ORIGINS = [
    'https://googleads.g.doubleclick.net',
    'https://static.doubleclick.net',
    'https://yt3.ggpht.com',
    'https://play.google.com',
]
# SESSION_COOKIE_DOMAIN = None

IMPORT_EXPORT_USE_TRANSACTIONS = True
SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {'lang': 'ru-RU'}
