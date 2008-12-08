import os

PROJECT_BASE = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('varikin', 'varikin@gmail.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_BASE, 'dev.db')

TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = os.path.join(PROJECT_BASE, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'ds(%#lzza1dpe1k@h@ikzuffk4cnr8zlldoms5dmrp!l7^k08s'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_BASE, 'templates'),    
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django_extensions',
    'django.contrib.flatpages', 
    'dali_flatpages',
    'gallery',
    'tagging',
    'blog',
)

FORCE_LOWERCASE_TAGS = True

try:
    from local_settings import *
except ImportError:
    pass
