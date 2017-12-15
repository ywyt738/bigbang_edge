"""
Production Configurations

- Use sentry for error logging

"""

import logging.config
from .base import *  # noqa
from os.path import join, dirname

# DEBUG
DEBUG = env.bool('DEBUG')

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])
# END SITE CONFIGURATION

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='产品创新部运维管理系统 <huangxj@ideal.sh.cn>')
EMAIL_SUBJECT_PREFIX = env(
    'DJANGO_EMAIL_SUBJECT_PREFIX', default='[测试]')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
INSTALLED_APPS += ['anymail', ]
ANYMAIL = {
    'MAILGUN_API_KEY': 'key-1c90d68f80a6e1fbb253da406177195d',
    'MAILGUN_SENDER_DOMAIN': 'sandbox44260bbadbe84eb5a9edee66bf9c310b.mailgun.org'
}
# EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp-ent.21cn.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'huangxj@ideal.sh.cn'
EMAIL_HOST_PASSWORD = 'ywyt135141!'
# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES['default'] = env.db('DATABASE_URL')


# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'

# Log everything to the logs directory at the top
LOGFILE_ROOT = join(dirname(BASE_DIR), 'logs')

# Reset logging
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'DEBUG',
        },
        'django.template': {
            'level': 'INFO',
        },
    }
}

logging.config.dictConfig(LOGGING)
