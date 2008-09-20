from django.http import Http404
from django.shortcuts import render_to_response
from dali.models import Picture, Gallery

def gallery_detail(request, gallery_):
    """View to show a specific gallery."""
    try:
        gallery = Gallery.objects.get(web_name__exact = gallery_)
        pictures = Picture.objects.filter(gallery = gallery).order_by('order')
    except Gallery.DoesNotExist:
        raise Http404

    return render_to_response('dali/gallery_detail.html', {'gallery': gallery, 'pictures': pictures})

def picture_detail(request, gallery_, picture_):
    """View to show a specific picture."""
    try:
        picture = Picture.objects.get(web_name__exact = picture_)
    except Picture.DoesNotExist:
        raise Http404

    return render_to_response('dali/picture_detail.html', {'picture': picture})
