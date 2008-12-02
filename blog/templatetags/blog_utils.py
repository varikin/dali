import re
from BeautifulSoup import BeautifulSoup
from django.db.models import Q
from django.template import Library, Node, TemplateSyntaxError 
import settings
from blog.models import Post
from gallery.models import Picture

register = Library()

@register.tag(name='get_latest_post')
def do_get_latest_post(parser, token):
    """
    This will store the latest post in the context.

    Usage:

        {% get_latest_post as post %}
        {{ post.title }}
        {{ post.body }}
    """
    tokens = token.contents.split()
    if len(tokens) != 3 or tokens[1] != 'as':
        raise TemplateSyntaxError("'get_latest_post' requires 'as variable' (got %r)" % args)
    return GetLatestPostNode(tokens[2]) 
    

class GetLatestPostNode(Node):
    def __init__(self, var):
        self.var = var
    
    def render(self, context):
        context[self.var] = Post.objects.filter(published=True)[0] #the order_by on model already gets latest
        return u''

@register.simple_tag
def image_preview(post, count):
    """
    Returns the first `count` images in the post body.  
    
    Usage:
        
        {% image_preview post 5 %}
    
    This also tries to replace the url for the images with thumbnail if possible.
    Checks if the image is flickr image or a local image and replaces it with 
    the appriate url.blog
    """
    soup = BeautifulSoup(post.body)
    imgs = soup('img', limit=count)
    methods = (_get_flickr_url, _get_local_url)
    if len(imgs) != 0:
        for img in imgs:
            for method in methods:
                src = method(img['src'])
                if src:
                    img['src']
                    break
           
            img['width'] = 75
            img['height'] = 75

        return ''.join([unicode(img) for img in imgs])
    else:
        return u''


def _get_local_url(url):
    """
    Returns the url to the thumbnail for a picture if the given url is to a
    picture in the Gallery app.  If not, returns None.
    """
    if url.startswith(settings.MEDIA_URL):
        path = url[len(settings.MEDIA_URL):]
        
        try:
            local = Picture.objects.get(Q(thumbnail=path) | Q(viewable=path) |
                Q(original=path))
            return local.thumbnail.url
        except Picture.DoesNotExist:
            return None

#Regex for Flickr url, see http://www.flickr.com/services/api/misc.urls.html
flickr_exp = r'''
    (?P<beginning>          #start the beginning of the url group
    http://
    (farm\d+\.)?            #farm id
    static.flickr.com/
    \d+/                    #server id
    \d+_                    #image id
    [a-zA-Z0-9]+            #image secret
    )                       #end the beginning of the url group
    (?P<suffix>(_[stmb])?)  #image type
    (?P<end>\.jpg)          #the end of the url group
    '''
flickr_url = re.compile(flickr_exp, re.VERBOSE)

def _get_flickr_url(url):
    """
    Returns the url to the square thumbnail on flickr if the given url is to a 
    flickr image. If not a flickr url, returns None.
    """
    match = flickr_url.match(url)
    if match:
        return '%s_s%s' % (match.group('beginning'), match.group('end'))
    else:
        return None
