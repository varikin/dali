from django.conf.urls.defaults import *
from blog.models import Post

date_based = {
    'date_field': 'date_published',
    'queryset': Post.objects.published(),
}
latest = dict(date_based)
archive = dict(date_based, **{'template_object_name': 'post'})

urlpatterns = patterns('django.views.generic.date_based',
    url(r'^$', 'archive_index', latest, name='blog_post_index'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 
        'archive_day', archive, name='blog_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 
        'archive_month', archive, name='blog_archive_month'),
    url(r'^(?P<year>\d{4})/$', 
        'archive_year', archive, name='blog_archive_year'),
)


post_detail = {
    'queryset': Post.objects.all(),
    'template_object_name': 'post',  
}

urlpatterns += patterns('',
    url(r'^(?P<slug>[-\w]+)/update/$', 'blog.views.update_post', name='blog_update_post'),
    url(r'^(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', 
        post_detail, name='blog_post_detail'),
)
