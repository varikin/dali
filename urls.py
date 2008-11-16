from django.conf.urls.defaults import *
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^blog/', include('blog.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^gallery/', include('gallery.admin.urls')),
    (r'^gallery/', include('gallery.urls')),
)

#Static serve
if settings.DEBUG:
    import os.path
    media = {'document_root': os.path.join(settings.PROJECT_BASE, 'media')}
    static = {'document_root': os.path.join(settings.PROJECT_BASE, 'static')}
    urlpatterns += patterns('django.views.static',
	    (r'^media/(?P<path>.*)$', 'serve', media),
	    (r'^static/(?P<path>.*)$', 'serve', static), 
    )
