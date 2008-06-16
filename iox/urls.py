from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
	(r'^music/', include('iox.music.urls')),
	(r'^blag/', include('iox.blag.urls')),
)
