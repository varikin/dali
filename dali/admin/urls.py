from django.conf.urls.defaults import *

#dali.views views
urlpatterns = patterns('dali.views',
    url(r'^/picture/save_order/$', 'save_picture_order', name='save_picture_order'),	
)
