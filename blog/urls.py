from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed
from blog.feeds import LatestPosts
from blog.models import Post
from blog.views import post_list, post_detail, update_post

posts = {
    'template_object_name': 'post' 
}

feeds = {
    'latest': LatestPosts,
}

urlpatterns = patterns('',
    url(r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feeds}),
    url(r'^(?P<slug>[-\w]+)/update/$', update_post, name='blog_update_post'),
    url(r'^(?P<slug>[-\w]+)/$', post_detail, posts, name='blog_post_detail'),
    url(r'^$', post_list, posts, name='blog_post_index'),
)
