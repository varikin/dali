from django.conf.urls.defaults import *
from blog.models import Post

tag_dict = {
    'queryset_or_model': Post,
    'related_tags': True,
    'template_name': 'blog/post_tag_list.html',
    'template_object_name': 'post',
}

cloud_template = {
    'template': 'blog/tag_cloud.html',
}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', cloud_template, 
        name='blog_tag_cloud'),
    url(r'^(?P<tag>[^/]+)/$', 'tagging.views.tagged_object_list', tag_dict, 
        name='blog_tag_detail'),
)