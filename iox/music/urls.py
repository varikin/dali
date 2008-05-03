from django.conf.urls.defaults import *
from iox.music.models import Song

info_dict = {
	'queryset': Song.objects.all()
}

# The generic views
urlpatterns = patterns('django.views.generic',
	(r'^$', 'list_detail.object_list', info_dict),
)

# The customer views
#urlpatterns += patterns('iox.music.views',
#	(r'^$', 'stuff'),
#)