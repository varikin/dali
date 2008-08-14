from django.conf.urls.defaults import *
from dali.models import Gallery

gallery_dict = {
	'queryset': Gallery.objects.filter(published=True),
}


#Generic views
urlpatterns = patterns('django.views.generic.list_detail',
	(r'^/$', 'object_list', gallery_dict),
)

#blag.views views
urlpatterns += patterns('dali.views',
	(r'^/(?P<webName>\w+)$', 'gallery_detail'),
)


