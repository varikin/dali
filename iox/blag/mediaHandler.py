from iox.blag.models import Media, Folder, Image, 
from os import path
from django import newforms as forms
from django

class MediaField(forms.FileField):
	


def createImage(image):
	validImage = validateImage(image)
	
	
def validateImage(image):
	valid = True

	if not image['content-type'].startsWidth('image'):
		valid = False

	fileExtensions = ('.jpg', '.jpeg', '.png')
	if path.splitext(image['filename'])[1].lower() not in fileExentions:
		valid = False
	
	return valid
	
	
	
	
	
	
