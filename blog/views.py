import logging
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from blog.models import Post

@permission_required('blog.change_post')
def update_post(request, slug):
    """Updates a post title. Permission required"""
    status = u'Failure'
    if request.method == 'POST':
        try:
            post = Post.objects.get(slug=slug)
            keys = request.POST.keys()
            updated = False
            for key in keys:
                value = request.POST.get(key).strip()
                if hasattr(post, key):
                    setattr(post, key, value)
                    updated = True
                else:
                    logging.warn("Error, %s part of Post" % key)
            
            if updated:
                post.save()
                status = u'Success'
        except (KeyError, Post.DoesNotExist):
            logging.error("Error, no post with slug: %s" % slug)
    else:
        loggiing.error("Error, not a HTTP POST")
        
    return HttpResponse(status, mimetype="text/plain")