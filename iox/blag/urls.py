from django.conf.urls.defaults import *
from iox.blag.models import *

info_dict = {
	'queryset': Image.objects.all()
}

# The generic views
urlpatterns = patterns('django.views.generic',
	(r'^$', 'list_detail.object_list', info_dict),
)