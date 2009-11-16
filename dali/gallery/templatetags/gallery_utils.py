from django.template import Library, Node, TemplateSyntaxError 
from gallery.models import Picture

register = Library()

@register.inclusion_tag('admin/gallery/reorder.html')
def register_reorder(callback):
    return {'drop_callback': callback}

@register.filter
def caption(picture):
    """
    Filter to format the caption for a picture.
    
    Usage: {{ picture|caption }}
    
    If an object without a name or desciption is used, an empty string is returned.
    """
    if hasattr(picture, 'name') and hasattr(picture, 'description'):
        return '<a href="%s">%s</a><p>%s</p>' % \
            (picture.get_absolute_url(), picture.name, picture.description or '')
    else:
        return ''
caption.is_safe = True

@register.tag(name='get_random_pictures')
def do_get_random_pictures(parser, token):
    """
    This will store random pictures in the context.

    Usage:

        {% get_random_pictures from gallery as pictures limit 5 %}
        {% for picture in pictures %}
        ...
        {% endfor %}
    """
    tokens = token.contents.split()
    if len(tokens) != 7 or tokens[1] != u'from' or tokens[3] != u'as' or \
        tokens[5] != u'limit':
        raise TemplateSyntaxError(
            "'get_random_pictures' requires 'from gallery as variable limit number' (got %r)" % tokens)
    try:
        count = int(tokens[6])
    except ValueError:
        raise TemplateSyntaxError(
            "'get_random_pictures' requires an integer as the last parameter (got %r)"
            % tokens[6])
    return GetRandomPictures(tokens[2], tokens[4], count)

class GetRandomPictures(Node):
    def __init__(self, gallery, var, count):
        self.gallery = gallery
        self.count = count
        self.var = var

    def render(self, context):
        context[self.var] = \
            Picture.objects.filter(gallery=context[self.gallery]).order_by('?')[:self.count]
        return u''

@register.tag(name='get_latest_pictures')
def do_get_latest_pictures(parser, token):
    """
    This will store the latest pictures in the context.

    Usage:

        {% get_latest_pictures as pictures limit 20 %}
        {% for picture in pictures %}
        ...
        {% endfor %}
    """
    tokens = token.contents.split()
    if len(tokens) != 5 or tokens[1] != u'as' or tokens[3] != u'limit':
        raise TemplateSyntaxError(
            "'get_latest_pictures' requires 'as variable limit number' (got %r)" % tokens)
    try:
        count = int(tokens[4])
    except ValueError:
        raise TemplateSyntaxError(
            "'get_latest_pictures' requires an integer as the last parameter (got %r)"
            % tokens[4])
    return GetLatestPictures(count, tokens[2]) 
    

class GetLatestPictures(Node):
    def __init__(self, count, var):
        self.count = count
        self.var = var
    
    def render(self, context):
        context[self.var] = Picture.objects.filter(gallery__published=True). \
            order_by('-date_created')[:self.count]
        return u''