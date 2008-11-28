from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from gallery.admin.forms import ZipFileForm
from gallery.models import Picture, Preferences

@permission_required('gallery.add_picture')
def add_pictures_from_zip(request):
    if request.method == 'POST':
        form = ZipFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/gallery/picture/')
    else:
        form = ZipFileForm()        
    
    response = {'form': form, 'title': 'Upload Multiple Pictures'}
    return render_to_response('admin/gallery/Picture/upload_zip_file.html', response)          

@permission_required('gallery.change_picture')
def save_picture_order(request):
    """
    Ajax POST view to save the order of a list of pictures.
    
    If the request is made via POST and is Ajax (XMLHttpRequest) by an
    authenticated user, the order for a list of pictures in POST QueryDict 
    is saved.  
    
    The QueryDict needs to contain a picture primary keys as the dict key and
    the order as the dict value.  Due to HTTP issues, both the keys and 
    values should unicode strings instead of ints.
    
    Note that this disables image generation for the saves.
    """
    if request.method == 'POST' and request.is_ajax():
        #Prevent image generation
        pref = Preferences.objects.get_preference()
        generate = pref.generate_images
        if generate:
            pref.generate_images = False
            pref.save()
        
        pictures = Picture.objects.filter(pk__in=request.POST.keys())
        for picture in pictures:
            picture.order = request.POST.get(unicode(picture.id))
            picture.save()
        
        #Revert image generation
        if generate:
            pref.generate_images = True
            pref.save() 

    return HttpResponse(None, mimetype='application/javascript')