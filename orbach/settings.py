'''
Copyright 2015

This file is part of Orbach.

Orbach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Orbach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Orbach.  If not, see <http://www.gnu.org/licenses/>.
'''

"""
Django 1.8 settings for Orbach project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import os
import sys

from io import StringIO

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from orbach.config import Config


ORBACH_DEFAULT_CONFIG = ("""
[orbach]
application_root = /var/lib/orbach
image_directory = images
gallery_directory = galleries
thumbnail_height = 250
thumbnail_width = 250
log_level = INFO
""")


def load_orbach_config():
    try:
        conf_file = os.environ['ORBACH_CONFIG']
        conf_file = os.path.expanduser(conf_file)
        fh = open(conf_file, 'r')
    except KeyError:
        error_msg = "Set the %s environment variable" % 'ORBACH_CONFIG'
        raise ImproperlyConfigured(error_msg)
    except IOError:
        error_msg = "Could not open file %s" % conf_file
        raise ImproperlyConfigured(error_msg)

    orbach_config = Config(fh)
    default_config = Config(StringIO(ORBACH_DEFAULT_CONFIG))

    for k, v in orbach_config.reserved_config().items():
        setattr(sys.modules[__name__], k, v)

    if 'SECRET_KEY' not in orbach_config.reserved_config().keys():
        raise ImproperlyConfigured("'SECRET_KEY' must be set in your orbach config file!")

    for k, v in default_config:
        if k not in orbach_config:
            orbach_config[k] = v

    return orbach_config


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'orbach_rjy0kjvzx-$ztd-q_zdt*pv3&tf=q3h5!#(f!gx-8th7hee31^'
DEBUG = False

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'orbach.urls'
WSGI_APPLICATION = 'orbach.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

# Load the conf file
ORBACH = load_orbach_config()

ORBACH_ROOT = os.path.expanduser(ORBACH['application_root'])

# Django options that should be immutable from the user perspective
# The user can set these in the conf file, but anything they set will be
# overwritten
MEDIA_ROOT = os.path.join(ORBACH_ROOT, ORBACH['image_directory'])

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'guardian',
    'django_bcrypt',
    'crispy_forms',
    'static_precompiler',
    'orbach.core',
    'orbach.gallery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ORBACH_ROOT, 'orbach.sqlite3'),
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'static_precompiler.finders.StaticPrecompilerFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'gallery', 'static'),
)

STATIC_ROOT = os.path.join(ORBACH_ROOT, 'static')

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'core', 'locale'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'orbach.core.permissions.OrbachObjectPermissions',
    ],
    'PAGE_SIZE': 20,
}

if DEBUG:
    ORBACH['log_level'] = "DEBUG"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] (%(name)s:%(module)s:%(lineno)d) %(message)s'
        },
        'simple': {
            'format': '%(asctime)s [%(levelname)s] (%(name)s) %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(ORBACH_ROOT, 'logs'),
            'maxBytes': 5000000,
            'backupCount': 2,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'orbach': {
            'handlers': ['console', 'file'],
            'level': ORBACH['log_level'],
        }
    }
}
