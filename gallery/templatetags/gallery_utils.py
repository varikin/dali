from django.template import Library, Node, TemplateSyntaxError 
from gallery.models import Picture

register = Library()

@register.tag(name='get_latest_pictures')
def do_get_latest_pictures(parser, token):
    """
    This will store the latest pictures in the context.

    Usage:

        {% get_latest_pictures 20 as pictures %}
        {% for picture in pictures %}
        ...
        {% endfor %}
    """
    tokens = token.contents.split()
    if len(tokens) != 4 or tokens[2] != 'as':
        raise TemplateSyntaxError("'get_latest_pictures' requires 'number as variable' (got %r)" % args)
    try:
        count = int(tokens[1])
    except ValueError:
        raise TemplateSyntaxError(
            "'get_latest_pictures' requires an integer as the first parameter (got %r)"
            % tokens[1])
    return GetLatestPictures(count, tokens[3]) 
    

class GetLatestPictures(Node):
    def __init__(self, count, var):
        self.count = count
        self.var = var
    
    def render(self, context):
        context[self.var] = Picture.objects.filter(gallery__published=True). \
            order_by('-date_created')[:self.count]
        return u''