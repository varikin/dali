from django.conf.urls.defaults import *
from blog.models import Post
from blog.views import post_list, post_detail, update_post

post_dict = {
    'template_object_name': 'post' 
}

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/update/$', update_post, name='blog_update_post'),
    url(r'^(?P<slug>[-\w]+)/$', post_detail, post_dict, name='blog_post_detail'),
    url(r'^$', post_list, post_dict, name='blog_post_index'),
)
