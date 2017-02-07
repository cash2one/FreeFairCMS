"""
Django settings for floodgaming project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
secret_file = open(os.path.join(os.path.dirname(__file__),'secret_keys.json'),'r').read()

SECRETS = json.loads(secret_file)
SECRET_KEY = SECRETS['django_key'] 


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'sass_processor',
    'mptt',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',
    'allauth',
    'allauth.account',
    'django_extensions',
    'bakery',
    'shared',
    'editors',
    'pages'
]


MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'base_templates')],
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

WSGI_APPLICATION = 'freefair.wsgi.application'


DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'freefair_db',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
    }
}


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
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'base_static'),
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# DJANGO USER SETTINGS
AUTH_USER_MODEL = 'editors.Editor'


# django-cors-headers configuration
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
CORS_REPLACE_HTTPS_REFERER = True
#CORS_ORIGIN_WHITELIST = (
#    'dashboard.floodgaming.com',
#    'localhost:9000'
#)

CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken',
        'access-control-allow-credentials'
    )


# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_PASSWORD_MIN_LENGTH = 8

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'editors.serializers.EditorDetailsSerializer',
}  

# ReCaptcha Settings
RECAPTCHA_PUBLIC_KEY = '6LfJgBIUAAAAAOsXSQ43N_CMiqKDhwLDEEWAbaHs'
RECAPTCHA_PRIVATE_KEY = SECRETS['recaptcha_key']


# Python-postmark settings
POSTMARK_API_KEY = SECRETS['postmark_key']
POSTMARK_SENDER = 'info@freefairunfettered.org'
DEFAULT_FROM_EMAIL = 'info@freefairunfettered.org'

# Django-bakery settings
BUILD_DIR = os.path.join(BASE_DIR, 'output/')
BAKERY_VIEWS = [
    'pages.views.SinglePageView',
    'pages.views.IndexView'
]

# Netlify settings
NETLIFY_TOKEN = SECRETS['netlify_access_token']
