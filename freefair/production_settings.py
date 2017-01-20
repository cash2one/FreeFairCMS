import os

from .base_settings import *

# Dev Environment specific settings
DEBUG = False
ALLOWED_HOSTS = ['104.236.84.60', '.freefairunfettered.org', '.freefairunfettered.com']

#Staticfiles settings
STATIC_ROOT = '/srv/freefairstatic' 
MEDIA_ROOT = '/srv/freefairmedia' 

# Development URLs
ROOT_URLCONF = 'freefair.production_urls'

# Rest Framework settings
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [ 'rest_framework.permissions.IsAuthenticated' ]

# Email config
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'watched_file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/freefair.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['watched_file',],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
