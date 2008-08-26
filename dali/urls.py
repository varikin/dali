from django.conf.urls.defaults import *
from dali.models import Gallery

gallery_dict = {
	'queryset': Gallery.objects.filter(published=True),
}


#Generic views
urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^/$', 'object_list', gallery_dict, name='gallery-list'),
    
)

#blag.views views
urlpatterns += patterns('dali.views',
    url(r'^/(?P<gallery_>\w+)/(?P<picture_>\w+)$', 'picture_detail', name='picture-detail'),	
    url(r'^/(?P<gallery_>\w+)$', 'gallery_detail', name='gallery-detail'),
)


