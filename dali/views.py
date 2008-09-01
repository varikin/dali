# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404
from dali.models import Picture, Gallery

def gallery_detail(request, gallery_):

	try:
		gallery = Gallery.objects.get(webName__exact = gallery_)
		pictures = Picture.objects.filter(gallery = gallery).order_by('order')
	except Gallery.DoesNotExist:
		raise Http404
	
	return render_to_response('dali/gallery_detail.html', {'gallery': gallery, 'pictures': pictures})

def picture_detail(request, gallery_, picture_):
    try:
        picture = Picture.objects.get(webName__exact = picture_)
    except Picture.DoesNotExist:
        raise Http404

    return render_to_response('dali/picture_detail.html', {'picture': picture})