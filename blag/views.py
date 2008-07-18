# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404
from blag.models import Image, Gallery

def gallery_detail(request, webName):

	try:
		gallery = Gallery.objects.get(webName__exact = webName)
		images = Image.objects.filter(gallery = gallery).order_by('order')
	except Gallery.DoesNotExist:
		raise Http404
	
	return render_to_response('blag/galleryDetail.html', {'gallery': gallery, 'images': images})