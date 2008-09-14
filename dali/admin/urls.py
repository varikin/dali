from django.conf.urls.defaults import *

#dali.views views
urlpatterns = patterns('dali.admin.views',
    url(r'^picture/save_order/$', 'save_picture_order', name='save_picture_order'),
    url(r'^picture/add_from_zip/$', 'add_pictures_from_zip', name='add_pictures_from_zip')	
)
