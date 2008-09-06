from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from dali.models import Picture, Preferences, Gallery

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
  
def save_order(request):
    """
    Ajax POST view to save the order of a list of pictures.
    
    If the request is made via POST and is Ajax (XMLHttpRequest) by an 
    authenticated user, the order for a list of pictures in POST QueryDict
    is saved.  
    
    The QueryDict should contain a picture primary keys as the 
    dict key and the order as the dict value.  Due to HTTP issues,
    both the keys and values should unicode strings instead of ints,
    
    Note that this does not generate images.
    """
    if request.method == 'POST' and request.is_ajax():
        #Prevent generating images
        pref = Preferences.objects.get_preference()
        generate = pref.generate_images
        if(pref.generate_images):
            pref.generate_images = False
            pref.save()
        
        pictures = Picture.objects.filter(pk__in=request.POST.keys())
        for picture in pictures:
            picture.order = request.POST.get(unicode(picture.id))
            picture.save()
        
        #Revert preference
        if(generate):
            pref.generate_images = True
            pref.save() 

    return HttpResponse(None, mimetype='application/javascript')
