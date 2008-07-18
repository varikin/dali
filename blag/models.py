from django.db import models
import os

class Gallery(models.Model):
	name = models.CharField(max_length = 200)
	webName = models.CharField(max_length = 200, unique = True)
	description = models.TextField()
	parentGallery = models.ForeignKey('self', null = True, blank = True)
	
	def __unicode__(self):
		return self.name
	
	def getRandomImage(self):
	    try:
	        image = Image.objects.filter(gallery = self).order_by('?')[0:1].get()
	    except Image.DoesNotExist:
	        image = None
	    
	    return image
	
	def getImageCount(self):
	    """
	    Returns the number of images in the gallery; return an integer
	    """
	    count = Image.objects.filter(gallery = self).count()
	    return count

	getImageCount.short_description = 'Number of Images'
	
	class Admin:
		list_display = ('name', 'webName', 'getImageCount', 'parentGallery')
		search_fields = ('name', 'webName',)

class Image(models.Model):
	name = models.CharField(max_length = 200)
	webName = models.CharField(max_length = 200, unique = True)
	original = models.ImageField(upload_to = "original")
	viewable = models.ImageField(upload_to = "viewable")
	thumbnail = models.ImageField(upload_to = "thumbnail")
	description = models.TextField()
	gallery = models.ForeignKey(Gallery)
	order = models.PositiveSmallIntegerField()
	
	def __unicode__(self):
		return self.name
	
	class Admin:
	    pass
