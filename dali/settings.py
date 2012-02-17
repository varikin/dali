import os
import logging


PROJECT_BASE = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('varikin', 'varikin@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    }
}

TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = os.path.join(PROJECT_BASE, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_BASE, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
	os.path.join(PROJECT_BASE, 'templates', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'ds(%#lzza1dpe1k@h@ikzuffk4cnr8zlldoms5dmrp!l7^k08s'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (

    'django.middleware.common.CommonMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

)

ROOT_URLCONF = 'dali.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_BASE, 'templates'),    
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    
    'django_extensions',
    'south',
    'djcelery',
    'ckeditor',
    
    'dali.dali_flatpages',
    'dali.gallery',
)

LOGGING = { 
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }   
    },  
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },  
    }   
}

# Gallery settings

GALLERY_THUMBNAIL_SIZE = 75
GALLERY_VIEWABLE_SIZE = 400
GALLERY_IMAGE_TYPE = 'JPEG'

# Cellary setting
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
		['Cut','Copy','Paste','PasteText','PasteFromWord','-', 'SpellChecker', 'Scayt'],
     		['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
     		['Link','Unlink','Anchor', 'Image', 'MediaEmbed'],
     		['HorizontalRule','Smiley','SpecialChar','PageBreak'],
     		['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
     		['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
     		['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
     		['Styles','Format','Font','FontSize'],
     		['TextColor','BGColor'],
     		['Maximize', 'ShowBlocks', 'Source']
        ],
        'width': 840,
        'height': 300,
        'toolbarCanCollapse': False,
		'filebrowserImageBrowseUrl': '/gallery/choose_picture/',
    }
}

try:
    from local_settings import *
except ImportError:
    pass
