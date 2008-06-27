from blag.models import Gallery, Image, Folder, Media
import StringIO
from PIL import Image as PImage

def createGallery(name, webName, description, parent):
	gallery = Gallery()
	gallery.name = name
	gallery.webName = webName
	gallery.description = description
	gallery.parentGallery = getObject(Gallery, parent)
	gallery.save()
	return gallery

def getObject(model, objectId):
	if ( objectId is not None ) and ( objectId is not u'' ):
		object = model.objects.get(id = objectId)
	else:
	    object = None
	
	return object

def createImage(name, webName, description, gallery, imageFile):
	image = PImage.open( StringIO.StringIO(imageFile['content'] ))
	
	original = createOriginal(imageFile['filename'], image)
	thumbnail = createThumbnail(imageFile['filename'], image)
	viewable = createViewable(imageFile['filename'], image)
	
	image = Image()
	image.name = name
	image.webName = webName
	image.original = original
	image.thumbnail = thumbnail
	image.viewable = viewable
	image.description = description
	image.gallery = getObject(Gallery, gallery)
	image.order = 1
	image.save()
	return image


def createOriginal(imageName, image):
	original = Media()
	original.name = "o_" + imageName 
	original.folder = getFolder()
	original.saveFile( image )
	original.save()
	return original

def createThumbnail(imageName, image):
	thumb = Media()
	thumb.name = "t_" + imageName
	thumb.folder = getFolder()
	thumb.saveFile( image.resize( (80, 80), PImage.ANTIALIAS ))
	thumb.save()
	return thumb

def createViewable(imageName, image):
	view = Media()
	view.name = "v_" + imageName
	view.folder = getFolder()
	view.saveFile( image.resize( (400, 400), PImage.ANTIALIAS ))
	view.save()
	return view 

def getFolder():
	folder = getObject(Folder, 2)
	return folder
