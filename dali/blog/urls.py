from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed
from blog.feeds import LatestPosts
from blog.models import Post
from blog.views import post_list, post_detail, update_post

feeds = {
    'latest': LatestPosts,
}

urlpatterns = patterns('',
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feeds}, name='blog_feed'),
    url(r'^(?P<slug>[-\w]+)/update/$', update_post, name='blog_update_post'),
    url(r'^(?P<slug>[-\w]+)/$', post_detail, {
        'template_object_name': 'post',
    }, name='blog_post_detail'),
    url(r'^$', post_list, {
        'template_object_name': 'post',
        'paginate_by': 10,
    }, name='blog_post_index'),
)
