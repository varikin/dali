# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404
from dali.models import Picture, Gallery

def gallery_detail(request, webName):

	try:
		gallery = Gallery.objects.get(webName__exact = webName)
		Pictures = Picture.objects.filter(gallery = gallery).order_by('order')
	except Gallery.DoesNotExist:
		raise Http404
	
	return render_to_response('dali/galleryDetail.html', {'gallery': gallery, 'Pictures': Pictures})
