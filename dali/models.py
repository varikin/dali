from __future__ import division
import os
import tempfile
import Image
from django.core.validators import ValidationError
from django.core.files import File
from django.db import models
from dali.managers import PreferenceManager

class Gallery(models.Model):    
    name = models.CharField(max_length=200)
    webName = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    parentGallery = models.ForeignKey('self', null=True, blank=True)
    published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
    
    def random_picture(self):
        """
        Return a random picture from the gallery.  If no pictures are in the gallery, 
        None is returned.
        """
        try:
            return Picture.objects.filter(gallery=self).order_by('?')[0]
        except IndexError:
            return None
    
    def picture_count(self):
        """
        Return the number of pictures in the gallery; return an integer.
        """
        return Picture.objects.filter(gallery=self).count()
    picture_count.short_description = 'Number of Pictures'
        

class Picture(models.Model):
    name = models.CharField(max_length=200)
    webName = models.CharField(max_length=200, unique=True)
    original = models.ImageField(upload_to='original')
    viewable = models.ImageField(upload_to='viewable')
    thumbnail = models.ImageField(upload_to='thumbnail')
    description = models.TextField()
    gallery = models.ForeignKey(Gallery)
    order = models.PositiveSmallIntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('order',)
    
    def __unicode__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False):
        """
        Saves a Picture instance. Return True if a thumbnail and viewable is
        generated, False otherwise.
        """
        pref = Preferences.objects.get_preference()
        result = False
        if(self.id is None or pref.generate_images):
            thumb_width = pref.thumbnail_width
            view_width = pref.viewable_width
            orig = Image.open(self.original.path)
            name = os.path.basename(self.original.name)
            
            thumb_temp = _get_resized_image(orig, thumb_width)
    	    self.thumbnail.save(name, File(thumb_temp), False)
    	    thumb_temp.close()
            
    	    view_temp = _get_resized_image(orig, view_width)
            self.viewable.save(name, File(view_temp), False)
            view_temp.close()            

            result = True
        
        super(Picture, self).save(force_insert, force_update)    
        return result        
        
class Preferences(models.Model):
    thumbnail_width = models.PositiveSmallIntegerField()
    viewable_width = models.PositiveSmallIntegerField()
    generate_images = models.BooleanField(default=False)
    
    objects = PreferenceManager()
    
    def __unicode__(self):
        return u'Preferences'
    
    def save(self, force_insert=False, force_update=False):
        """
        Save the preference is it an existing preference or if there are not an 
        existing preference.  Only allowing one preference.
        """
        if(self.id is not None or Preferences.objects.count() == 0):
            super(Preferences, self).save(force_insert, force_update)
        else:
            raise ValidationError('Only one preference object allowed.')

def _get_resized_image(image, width):
    """
    Return a temporary file containing a resized image of a given PIL image.
    
    The height of the resized image is calculated based upon the original image
    size and the width so as to perserve the aspect ratio.
    
    The temporary file will be deleted automatically when closed. 
    """
    height = int(width * image.size[1] / image.size[0])
    resized = image.resize((width, height), Image.ANTIALIAS)
    tf = tempfile.NamedTemporaryFile('w+b')
    resized.save(tf, 'JPEG')
    return tf
