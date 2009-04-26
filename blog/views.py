import logging
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.views.generic import list_detail
from blog.models import Post
from blog.forms import PostForm

def privileged_post_queryset(view):
    """
    Decorator to set the Post queryset.
    
    If the user is authenticated, return all posts, else only the published posts.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            kwargs['queryset'] = Post.objects.all().order_by('-date_published')
        else:
            kwargs['queryset'] = Post.objects.published().order_by('-date_published')
        return view(request, *args, **kwargs)
    return _wrapped_view

post_list = privileged_post_queryset(list_detail.object_list)
post_detail = privileged_post_queryset(list_detail.object_detail)

@permission_required('blog.change_post')
def update_post(request, slug):
    """
    Updates a post for the given slug.

    For every key in the POST, tries to set a post attr with the key name.
    """
    status = u'Failure'
    if request.method == 'POST':
        try:
            post = Post.objects.get(slug=slug)
            form = PostForm(request.POST)
            keys = request.POST.keys()
            if form.is_valid():
                for key in keys:
                    setattr(post, key, form.cleaned_data[key])
                post.save()
                status = u'Success'
            else:
                logging.error('POST data not valid: %s' % request.POST)
        except (Post.DoesNotExist):
            logging.error("No post with slug: %s" % slug)
    else:
        logging.error("Not a HTTP POST")
    return HttpResponse(status, mimetype="text/plain")
