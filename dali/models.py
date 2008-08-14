from __future__ import division
import os
import tempfile
import Image
from django.core.files import File
from django.db import models

class Gallery(models.Model):
    name = models.CharField(max_length=200)
    webName = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    parentGallery = models.ForeignKey('self', null=True, blank=True)
    published = models.BooleanField(default=False)
        
    def __unicode__(self):
        return self.name
    
    def getRandomPicture(self):
        """
        Return a random picture from the gallery.  If not pictures are in the gallery, 
        None is returned.
        """
        try:
            picture = Picture.objects.filter(gallery = self).order_by('?')[0:1].get()
        except Picture.DoesNotExist:
            picture = None
        
        return picture
    
    def getPictureCount(self):
        """
        Return the number of pictures in the gallery; return an integer.
        """
        return Picture.objects.filter(gallery = self).count()
        
    getPictureCount.short_description = 'Number of Pictures'

class Picture(models.Model):
    name = models.CharField(max_length=200)
    webName = models.CharField(max_length=200, unique=True)
    original = models.ImageField(upload_to='original')
    viewable = models.ImageField(upload_to='viewable')
    thumbnail = models.ImageField(upload_to='thumbnail')
    description = models.TextField()
    gallery = models.ForeignKey(Gallery)
    order = models.PositiveSmallIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        """
        Saves a Picture instance.
        
        Generates a thumbnail and viewable from the original image using PIL.
        """
        orig = Image.open(self.original.path)
        name = os.path.basename(self.original.name)
        
        prefs = Preferences.objects.all()[0:1].get()
        thumb_width = prefs.thumbnail_width
        view_width = prefs.viewable_width
       
	
        thumb_temp = _get_resized_image(orig, thumb_width)
	self.thumbnail.save(name, File(thumb_temp), False)
        
	view_temp = _get_resized_image(orig, view_width)
        self.viewable.save(name, File(view_temp), False)
        
        super(Picture, self).save()
        
        thumb_temp.close()
        view_temp.close()
        

class Preferences(models.Model):
    thumbnail_width = models.PositiveSmallIntegerField()
    viewable_width = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return u'Preferences'
    
    def save(self):
        """
        Save the preference is it an existing preference or if there are not an 
        existing preference.  Only allowing one preference.
        """
        if(self.id is not None or Picture.objects.count() == 0):
            super(Preferences, self).save()



def _get_resized_image(image, width):
    """
    Return a temporary file containing a resized image.  
    
    The height of the resized image is calculated based upon the original image
    size and the width so as to perserve the aspect ratio.
    
    The temporary file will be deleted automatically when closed. 
    
    Parameters: 
    image: A PIL Image object
    size: The width in pixels to resize the image to.  
    
    """
    height = int(width * image.size[1] / image.size[0])
    resized = image.resize((width, height), Image.ANTIALIAS)
    tf = tempfile.NamedTemporaryFile('w+b')
    resized.save(tf, 'JPEG')
    return tf 
