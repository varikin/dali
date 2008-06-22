from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list 
from iox.blag.models import *

image_dict = {
	'queryset': Image.objects.all(),
}

gallery_dict = {
	'queryset': Gallery.objects.all(),
}

urlpatterns = patterns('',
	(r'^$', 'iox.blag.views.admin'),
	(r'^image$', 'object_list', image_dict),
	(r'^gallery$', 'object_list', gallery_dict),
	(r'^gallery/(?P<webName>\w+)$', 'iox.blag.views.galleryDetail'),
	(r'^create/gallery$', 'iox.blag.views.createGallery'),
	(r'^create/image$', 'iox.blag.views.createImage'),
)


