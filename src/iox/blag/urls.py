from django.conf.urls.defaults import *
from iox.blag.models import *

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

#iox.blag.views views
urlpatterns += patterns('iox.blag.views',
	(r'^$', 'admin'),
	(r'^gallery/(?P<webName>\w+)$', 'galleryDetail'),
	(r'^create/gallery$', 'createGallery'),
	(r'^create/image$', 'createImage'),
)


