import os

PROJECT_BASE = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('varikin', 'varikin@gmail.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_BASE, 'dev.db')
TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = os.path.join(PROJECT_BASE, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'

SECRET_KEY = 'm^e$b0(38%!tz592na&vx9g55w%m8m(@y0ooqq-rvsdj3nw-rf'

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
    'customflatpages',
    'gallery',
    'tagging',
    'blog',
)

FORCE_LOWERCASE_TAGS = True
