from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

import mobileadmin
mobileadmin.autoregister()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^ma/(.*)', mobileadmin.sites.site.root),
    (r'^blog/', include('blog.urls')),
    (r'^tag/', include('blog.tag_urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^gallery/', include('gallery.admin.urls')),
    (r'^gallery/', include('gallery.urls')),
)

handler404 = 'mobileadmin.views.page_not_found'
handler500 = 'mobileadmin.views.server_error'

#Static serve
if settings.DEBUG:
    from mobileADmin.conf import settings as ma_settings
    import os.path
    media = {'document_root': os.path.join(settings.PROJECT_BASE, 'media')}
    static = {'document_root': os.path.join(settings.PROJECT_BASE, 'static')}
    ma_static = {'document_root': ma_settings.MEDIA_PATH }
    urlpatterns += patterns('django.views.static',
	    (r'^media/(?P<path>.*)$', 'serve', media),
	    (r'^static/(?P<path>.*)$', 'serve', static),
	    (ma_settings.MEDIA_REGEX, 'serve', ma_static),
    )
