from iox.blag.models import Gallery

def createGallery(name, webName, description, parent):
	gallery = Gallery()
	gallery.name = name
	gallery.webName = webName
	gallery.description = description
	gallery.parentGallery = getObject(Gallery, parent)
	gallery.save()
	return gallery

def getObject(model, objectId):
	object = None
	if objectId is not None:
		object = model.objects.get(id = objectId)
	
	return object
