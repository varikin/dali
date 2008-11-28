from django.conf.urls.defaults import *
from gallery.models import Gallery

gallery_dict = {
	'queryset': Gallery.objects.filter(published=True),
}


#Generic views
urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', gallery_dict, name='gallery-gallery-list'),
    
)

#gallery.views views
urlpatterns += patterns('gallery.views',
    url(r'^(?P<gallery>[-\w]+)/(?P<picture>[-\w]+)$', 'picture_detail', name='gallery-picture-detail'),	
    url(r'^(?P<gallery>[-\w]+)$', 'gallery_detail', name='gallery-gallery-detail'),
)

