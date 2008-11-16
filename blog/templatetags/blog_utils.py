from BeautifulSoup import BeautifulSoup
from django.template import Library
from gallery.models import Preferences

register = Library()

@register.simple_tag
def image_preview(post, num_images):
    soup = BeautifulSoup(post.body)
    imgs = soup('img', limit=num_images)
    if len(imgs) != 0:
        pref = Preferences.objects.get_preference()
        for img in imgs:
            img['width'] = pref.thumbnail_width
            del(img['height']) 
        return ''.join([unicode(img) for img in imgs])
    else:
        return u''