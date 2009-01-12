from django.conf.urls.defaults import *
from gallery.models import Gallery
from gallery.views import *

gallery_dict = {
	'template_object_name': 'gallery'
}

#Generic views
urlpatterns = patterns('',
    url(r'^choose_picture/$', choose_gallery, name='gallery_choose_gallery'),
    url(r'^choose_picture/(?P<gallery>[-\w]+)/$', choose_picture, 
        name='gallery_choose_picture'),

    url(r'^$', gallery_list, gallery_dict, name='gallery_list'),   
    url(r'^(?P<gallery>[-\w]+)/$', gallery_detail, name='gallery_detail'),
    url(r'^(?P<gallery>[-\w]+)/(?P<picture>[-\w]+)/$', picture_detail, name='picture_detail'),
)


