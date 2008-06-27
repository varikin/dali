from django.conf.urls.defaults import *
from blag.models import *

image_dict = {
	'queryset': Image.objects.all(),
}

gallery_dict = {
	'queryset': Gallery.objects.all(),
}


#Generic views
urlpatterns = patterns('django.views.generic.list_detail',
	(r'^image$', 'object_list', image_dict),
	(r'^gallery$', 'object_list', gallery_dict),
)

#blag.views views
urlpatterns += patterns('blag.views',
    (r'^$', 'home'),
	(r'^admin$', 'admin'),
	(r'^gallery/(?P<webName>\w+)$', 'galleryDetail'),
	(r'^create/gallery$', 'createGallery'),
	(r'^create/image$', 'createImage'),
)


