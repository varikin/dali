from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Uncomment this for admin:
	(r'^', include('iox.blag.urls')),
)
