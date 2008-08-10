import os
import tempfile
import Image as PIL
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
    _dir = {'o': 'original', 'v': 'viewable', 't': 'thumbnail'}    
    name = models.CharField(max_length=200)
    webName = models.CharField(max_length=200, unique=True)
    original = models.ImageField(upload_to=_dir['o'])
    viewable = models.ImageField(upload_to=_dir['v'])
    thumbnail = models.ImageField(upload_to=_dir['t'])
    description = models.TextField()
    gallery = models.ForeignKey(Gallery)
    order = models.PositiveSmallIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def get_thumbnail_size(self):
        prefs = Preferences.objects.all()[0:1].get()
        return (prefs.thumbnail_width, prefs.thumbnail_height)
    
    def get_viewable_size(self):
        prefs = Preferences.objects.all()[0:1].get()
        return (prefs.viewable_width, prefs.viewable_height)
    
    def save(self):
        """
        Saves a Picture instance.
        
        Generates a thumbnail and viewable from the original image using PIL.
        """
        name = os.path.basename(self.original.name)
        orig = PIL.open(self.original.path)
        
        thumb_temp = _get_resized_image(orig, self.get_thumbnail_size())
        self.thumbnail.save(name, File(open(thumb_temp)), False)
        
        view_temp = _get_resized_image(orig, self.get_viewable_size())
        self.viewable.save(name, File(open(view_temp)), False)
        
        super(Picture, self).save()
        
        os.remove(view_temp)
        os.remove(thumb_temp)
        

class Preferences(models.Model):
    thumbnail_width = models.PositiveSmallIntegerField()
    thumbnail_height = models.PositiveSmallIntegerField()
    viewable_width = models.PositiveSmallIntegerField()
    viewable_height = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return u'Preferences'
    
    def save(self):
        """
        Save the preference is it an existing preference or if there are not an 
        existing preference.  Only allowing one preference.
        """
        if(self.id is not None or Picture.objects.count() == 0):
            super(Preferences, self).save()



def _get_resized_image(image, size):
    """
    Return temporary filename of resized image.
    
    The temporary file should be deleted when finished with it.
    
    Parameters: 
    image: A PIL Image object
    size: tuple for size of thumbnail e.g. (100, 100)
    
    Returns A path to a temp image file as a string.
    """
    resized = image.resize(size, PIL.ANTIALIAS)
    name = tempfile.mkstemp('.jpg') #make temp file with .jpg suffix
    resized.save(name[1])
    return name[1]