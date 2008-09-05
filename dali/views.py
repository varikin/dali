from django.shortcuts import render_to_response
from django.http import Http404
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
    
def save_picture_order(pictures):
    """
    Saves the order of a list of pictures. This does not generate images. A 
    ``TypeError`` is raised if ``pictures`` is not a list or tuple.
    """
    if(hasattr(pictures, '__iter__')):
        pref = Preferences.objects.get_preference()
        generate = pref.generate_images
        if(pref.generate_images):
            pref.generate_images = False
            pref.save()

        for picture in pictures:
            picture.save()

        if(generate):
            pref.generate_images = True
            pref.save()
    else:
        raise TypeError('List or tuple required')
