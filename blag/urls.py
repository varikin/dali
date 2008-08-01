from django.conf.urls.defaults import *
from blag.models import Gallery

gallery_dict = {
	'queryset': Gallery.objects.all(),
}


#Generic views
urlpatterns = patterns('django.views.generic.list_detail',
	(r'^/$', 'object_list', gallery_dict),
)

#blag.views views
urlpatterns += patterns('blag.views',
	(r'^/(?P<webName>\w+)$', 'gallery_detail'),
)


