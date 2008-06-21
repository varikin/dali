from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
	(r'^blag/', include('iox.blag.urls')),
)
