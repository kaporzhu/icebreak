# -*- coding: utf-8 -*-
"""
Django settings for icebreak project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-!$b%o=52+9r@@!rnwd7-@s(^jyp0j_)c(zxsaptyg2n==s0h!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

LOCAL_APPS = (
    'accounts',
    'buildings',
    'coupons',
    'foods',
    'icebreak',
    'orders',
    'portals',
    'shops',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd libs
    'compressor',
    'debug_toolbar',
    'easy_thumbnails',
    'south',
) + LOCAL_APPS

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations'
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'icebreak.urls'

WSGI_APPLICATION = 'icebreak.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = False

USE_L10N = False

USE_TZ = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

THUMBNAIL_ALIASES = {
    '': {
        'small': {
            'size': (128, 128)
        },
        'medium': {
            'size': (256, 256)
        },
        'large': {
            'size': (512, 512)
        },
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '/static/libs/jquery/jquery-1.11.1.min.js'
}

MASTER_KEY = ''
SMS_NOTIFICATION_ENABLED = False
SMS_SERVER_URL = 'http://106.ihuyi.cn/webservice/sms.php?method=Submit'
SMS_SERVER_USERNAME = ''
SMS_SERVER_PASSWORD = ''
SMS_TEMPLATES = {
    'validation_code': u'您的验证码是{}，三十分钟内有效',
    'order_reminder': u'您的订单已送出，点击链接查看最新进度 {}'
}

try:
    from local_settings import *  # noqa
except ImportError:
    pass
