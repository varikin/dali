from django.http import Http404
from django.shortcuts import render_to_response
from gallery.models import Picture, Gallery

def gallery_detail(request, gallery):
    """View to show a specific gallery."""
    context = {}
    try:
        context['gallery'] = Gallery.objects.get(slug = gallery)
        context['pictures'] = \
            Picture.objects.filter(gallery = context['gallery']).order_by('order')
    except Gallery.DoesNotExist:
        raise Http404
    
    return render_to_response('gallery/gallery_detail.html', context)

def picture_detail(request, gallery, picture):
    """View to show a specific picture."""
    context = {}
    try:
        context['picture'] = Picture.objects.get(slug = picture)
    except Picture.DoesNotExist:
        raise Http404

    return render_to_response('gallery/picture_detail.html', context)
