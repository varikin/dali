from django.conf.urls.defaults import *
from gallery.models import Gallery

gallery_dict = {
	'queryset': Gallery.objects.filter(published=True),
	'template_object_name': 'gallery'
}


#Generic views
urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', gallery_dict, name='gallery_list'),   
)

#gallery.views views
urlpatterns += patterns('gallery.views',
    url(r'^choose_picture/$', 'choose_gallery', name='gallery_choose_gallery'),
    url(r'^choose_picture/chooser_status/$', 'chooser_status', name='gallery_chooser_status'),
    url(r'^choose_picture/(?P<gallery>[-\w]+)/$', 'choose_picture', 
        name='gallery_choose_picture'),
    url(r'^(?P<gallery>[-\w]+)/(?P<picture>[-\w]+)/$', 'picture_detail', 
        name='picture_detail'),	
    url(r'^(?P<gallery>[-\w]+)/$', 'gallery_detail', name='gallery_detail'),
)


