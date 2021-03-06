# -*- coding: utf-8 -*-
"""
Django settings for tbackup_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import settings_dev

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_dev.SECRET_KEY
R_SIGNATURE_KEY = settings_dev.R_SIGNATURE_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings_dev.DEBUG

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
from django.core.files.storage import default_storage
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'south',
    'django_extensions',
    'server',
)
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    )
}
SWAGGER_SETTINGS = {
    "exclude_namespaces": [],
    "api_version": '0.1',
    "api_path": "/",
    "enabled_methods": [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '',
    "is_authenticated": True,
    "is_superuser": True,
    "permission_denied_handler": None,
    "info": {
        'contact': '',
        'description': '',
        'license': '',
        'licenseUrl': '',
        'termsOfServiceUrl': '',
        'title': 'Tbackup-server API Docs',
    },
}

LOGIN_REDIRECT_URL = '/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

ROOT_URLCONF = 'tbackup_server.urls'

WSGI_APPLICATION = 'tbackup_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = settings_dev.DATABASES

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#TEMPLATE_DIRS = (
#    os.path.join(BASE_DIR, 'templates'),
#)

#TBackup Project's specific constants
DT_FORMAT = '%Y%m%d_%H%M'
DT_FORMAT_VERBOSE = u'%d/%m/%Y - %H:%M'
