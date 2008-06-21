from django.conf.urls.defaults import *
from iox.blag.models import *

image_dict = {
	'queryset': Image.objects.all(),
}

gallery_dict = {
	'queryset': Gallery.objects.all(),
}

urlpatterns = patterns('',
	(r'^image$', 'django.views.generic.list_detail.object_list', image_dict),
	(r'^gallery$', 'django.views.generic.list_detail.object_list', gallery_dict),
	(r'^gallery/(?P<webName>\w+)$', 'iox.blag.views.galleryDetail'),
	(r'^create/gallery$', 'iox.blag.views.createGallery'),
	(r'^create/image$', 'iox.blag.views.createImage'),
)


