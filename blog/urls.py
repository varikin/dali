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
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
        'object_detail', archive, name='blog_post_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 
        'archive_day', archive, name='blog_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 
        'archive_month', archive, name='blog_archive_month'),
    url(r'^(?P<year>\d{4})/$', 
        'archive_year', archive, name='blog_archive_year'),
)

tag_dict = {
    'queryset_or_model': Post,
    'related_tags': True,
    'template_name': 'blog/post_tag_list.html',
    'template_object_name': 'post',
}

cloud_template = {
    'template': 'blog/tag_cloud.html',
}

urlpatterns += patterns('',
    url(r'tags/$', 'django.views.generic.simple.direct_to_template', cloud_template, 
        name='blog_tag_cloud'),
    url(r'tags/(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', tag_dict, 
        name='blog_tag_detail'),
)
