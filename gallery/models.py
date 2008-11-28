from __future__ import division
import os
import tempfile
import Image
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models

class Gallery(models.Model):    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
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
    THUMBNAIL_WIDTH = 75
    VIEWABLE_WIDTH = 400
    IMAGE_TYPE = 'JPEG'

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    original = models.ImageField(upload_to='original')
    viewable = models.ImageField(upload_to='viewable')
    thumbnail = models.ImageField(upload_to='thumbnail')
    description = models.TextField(null=True, blank=True)
    gallery = models.ForeignKey(Gallery)
    order = models.PositiveSmallIntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    

    
    
    class Meta:
        ordering = ('order',)
    
    def __unicode__(self):
        return self.name
    
    def save(self, **kwargs):
        """
        Saves a Picture instance. Return True if a thumbnail and viewable is
        generated, False otherwise.
        """
        # Determine if this is a new picture object or new original file.
        generate_images = True
        if self.id is not None:
            old_picture = Picture.objects.get(pk=self.id)
            if self.original.path == old_picture.original.path:
                generate_images = False
                
        if generate_images:
            orig = Image.open(self.original.path)
            name = os.path.basename(self.original.name)
            _resize_image(self.thumbnail, orig, name, Picture.THUMBNAIL_WIDTH, Picture.IMAGE_TYPE)
            _resize_image(self.viewable, orig, name, Picture.VIEWABLE_WIDTH, Picture.IMAGE_TYPE)        
            result = True
        
        super(Picture, self).save(**kwargs)    
        return generate_images

def _resize_image(thumb, original, name, width, image_type):
    """
    Resizes an image.
    
    thumb - A ImageField for a model that will contain the resized image
    original - A PIL Image object
    name - A string to name the thumbnail
    width - The width of the resized image, the height is calculated from this.
    image_type - The type of image to save the thumb as.  Should be 'JPEG' or 'PNG'
    """
    height = int(width * original.size[1] / original.size[0])
    resized = original.resize((width, height), Image.ANTIALIAS)
    tf = tempfile.NamedTemporaryFile('w+b')
    resized.save(tf, image_type)
    thumb.save(name,File(tf), False)
    tf.close()
