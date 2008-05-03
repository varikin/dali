from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
	(r'^music/style/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/varikin/code/iox/music/templates/music/style'}),
	(r'^music/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/varikin/code/iox/music/templates/music/js'}),
	(r'^vault/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/varikin/code/iox/vault'}),
	(r'^music/', include('iox.music.urls')),
	(r'^blag/', include('iox.blag.urls')),
)
