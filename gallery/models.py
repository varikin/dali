from __future__ import division
import os
import tempfile
import Image
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from gallery.managers import PreferenceManager

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
        pref = Preferences.objects.get_preference()
        result = False
        if(self.id is None or pref.generate_images):
            orig = Image.open(self.original.path)
            name = os.path.basename(self.original.name)
            thumb_width = pref.thumbnail_width
            view_width = pref.viewable_width
            _resize_image(self.thumbnail, orig, name, thumb_width, pref.image_type)
            _resize_image(self.viewable, orig, name, view_width, pref.image_type)        
            result = True
        
        super(Picture, self).save(**kwargs)    
        return result
        
class Preferences(models.Model):
    IMAGE_CHOICES = (
        ('JPEG', 'JPEG'),
        ('PNG', 'PNG'),
    )
    
    thumbnail_width = models.PositiveSmallIntegerField()
    viewable_width = models.PositiveSmallIntegerField()
    generate_images = models.BooleanField(default=False)
    image_type = models.CharField(max_length=1, choices=IMAGE_CHOICES)
    
    objects = PreferenceManager()
    
    def __unicode__(self):
        return u'Preference'
    
    def save(self, **kwargs):
        """
        Save the preference is it an existing preference or if there are not an 
        existing preference.  Only allowing one preference.
        """
        if(self.id is not None or Preferences.objects.count() == 0):
            super(Preferences, self).save(**kwargs)
        else:
            raise ValidationError('Only one preference object allowed.')


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
