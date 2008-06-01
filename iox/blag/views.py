# Create your views here.
from django import newforms as forms
from django.shortcuts import render_to_response
from iox.blag.models import Image, Media, Gallery, Folder

class CreateImageForm(forms.Form):
	imageFile = forms.ImageField(label="Please choose an image file")
	
def uploadImage(request):
	if request.method == 'POST':
		form = CreateImageForm(request.POST, request.FILES)
		if request.FILES.has_key('imageFile'):
			filename = request.FILES['imageFile']['filename']
			if request.FILES['imageFile']['content-type'].startswith('image'):
				filename = '/Users/varikin/code/blag/iox/blag/gallery/thumbnail/i' + filename
				
	else:
		form = CreateImageForm()
	
	return render_to_response('blag/uploadImage.html', {'form': form, 'file': request.FILES})

def saveImage(image):
	filename = image['filename']
		