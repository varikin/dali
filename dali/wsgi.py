import os
import django.core.handlers.wsgi

os.environ['DJANGO_SETTINGS_MODULE'] = 'dali.settings'
application = django.core.handlers.wsgi.WSGIHandler()
