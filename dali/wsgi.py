import os
import django.core.handlers.wsgi

os.environ["CELERY_LOADER"] = "django"
os.environ['DJANGO_SETTINGS_MODULE'] = 'dali.settings'
application = django.core.handlers.wsgi.WSGIHandler()
