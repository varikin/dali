# Create your views here.
from django.shortcuts import render_to_response
from django.http import Http404
from blag.models import Image, Media, Gallery, Folder
from blag import handlers
        
def createImage(request):
	if request.method == 'POST':
		requiredValues = hasRequiredValues(request.POST, \
			[ 'name', 'description', 'webName', 'gallery' ])
		validImage = hasValidImage(request.FILES, 'imageFile')  
		if requiredValues and validImage:
			name = request.POST['name']
			description = request.POST['description']
			webName = request.POST['webName']
			gallery = request.POST['gallery']
			imageFile = request.FILES['imageFile']

			image = handlers.createImage(name, webName, description, gallery, imageFile)


	galleries = Gallery.objects.all()
	return render_to_response('blag/createImage.html', {'galleries': galleries})
	

def createGallery(request):
	if request.method == 'POST':
		requiredValues = ['name', 'description', 'webName']
		if hasRequiredValues(request.POST, requiredValues): 
			name = request.POST['name']
			description = request.POST['description']
			webName = request.POST['webName']
			parent = request.POST.get('parent', None)

			gallery = handlers.createGallery(name, webName, description, parent)

	
	galleries = Gallery.objects.all()

	return render_to_response('blag/createGallery.html', {'galleries': galleries})


def gallery_detail(request, webName):

	try:
		gallery = Gallery.objects.get(webName__exact = webName)
		images = Image.objects.filter(gallery = gallery).order_by('order')
	except Gallery.DoesNotExist:
		raise Http404
	
	return render_to_response('blag/galleryDetail.html', {'gallery': gallery, 'images': images})

def hasRequiredValues(post, requiredValues):
	result = True
	for requiredValue in requiredValues:
		if not post.has_key(requiredValue):
			result = False

	return result

def hasValidImage(files, imageName):
	result = False
	if files.has_key(imageName):
		if files[imageName]['content-type'].startswith('image'):
			result = True

	return result
