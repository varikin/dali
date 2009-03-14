from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from blog.models import Post

class LatestPosts(Feed):
    feed_type = Atom1Feed
    title = 'Jes Lee Photos'
    link = '/blog/'
    subtitle = 'Latest blog posts for Jes Lee Photos'
    
    def items(self):
        return Post.objects.published().order_by('-date_published')[:10]
