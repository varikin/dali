from django.conf.urls.defaults import *
from iox.blag.models import *

info_dict = {
	'queryset': Image.objects.all()
}

# The generic views
urlpatterns = patterns('',
	(r'^$', 'django.views.generic.list_detail.object_list', info_dict),
	(r'^/uploadImage', 'iox.blag.views.uploadImage'),
)