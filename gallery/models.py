from __future__ import division
import os
import tempfile
import Image
from django.core.files import File
from django.db import models
from gallery.managers import GalleryManager

class Gallery(models.Model):    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    parent_gallery = models.ForeignKey('self', null=True, blank=True)
    published = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    objects = GalleryManager()
    
    class Meta:
        verbose_name_plural = "galleries"
        ordering = ('order',)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ("gallery_detail", (), {"gallery": self.slug})
    
    def picture_count(self):
        """Returns the number of pictures in the gallery."""
        return Picture.objects.filter(gallery=self).count()
    picture_count.short_description = 'Number of Pictures'
        

class Picture(models.Model):
    THUMBNAIL_SIZE = 75
    VIEWABLE_SIZE = 400
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
    
    @models.permalink
    def get_absolute_url(self):
        return ("picture_detail", (), {
            "picture": self.slug, 
            "gallery": self.gallery.slug,
        })
    
    def save(self, **kwargs):
        """
        Saves a Picture instance. Return True if a thumbnail and viewable is
        generated, False otherwise.
        """
        
        # Determine if new file, if not, get path of old original image
        if self.id is not None:
            old_path = Picture.objects.get(pk=self.id).original.path
        else:
            old_path = None
        
        # Save before generating image
        # The uploaded images are not avalable till after saving
        super(Picture, self).save(**kwargs) 

        # Generate images if new Picture or change original file
        if old_path is None or self.original.path != old_path:
            orig = Image.open(self.original.path)
            name = os.path.basename(self.original.name)
            self.create_viewable(orig, name, save=True)
            self.create_thumbnail(orig, name, save=True)
            return True
        else: # The return is to ease testing
            return False
        
    def create_viewable(self, image=None, name=None, save=False):
        """
        Creates a viewable for a Picture.
        
        image: A PIL image.  If not given, opens the original with PIL.
        name: A name for the viewable.  If not given, uses basename of the 
            original
        save: Whether to save the object or not.
        """
        if image is None:
            image = Image.open(self.original.path)
        if name is None:
            name = os.path.basename(self.original.name)
        
        width, height = _get_viewable_size(image.size[0], image.size[1])
        resized = image.resize((width, height), Image.ANTIALIAS)
        tf = tempfile.NamedTemporaryFile('w+b')
        resized.save(tf, Picture.IMAGE_TYPE)
        self.viewable.save(name,File(tf), save)
        tf.close()
        
    def create_thumbnail(self, image=None, name=None, save=False):
        """
        Creates a thumbnail for a Picture.
        
        The thumbnail is cropped to be square.
        image: A PIL image.  If not given, opens the original with PIL.
        name: A name for the viewable.  If not given, uses basename of the 
            original
        save: Whether to save the object or not.
        """
        if image is None:
            image = Image.open(self.original.path)
        if name is None:
            name = os.path.basename(self.original.name)

        width, height = _get_thumbnail_size(image.size[0], image.size[1])
        resized = image.resize((width, height), Image.ANTIALIAS)

        lower, remainder = divmod(Picture.THUMBNAIL_SIZE, 2)
        upper = lower
        if remainder != 0: 
            upper += 1

        if width > height:
            center = resized.size[0] // 2
            box = (center - lower, 0, center + upper, Picture.THUMBNAIL_SIZE)
        else:
            center = resized.size[1] // 2
            box = (0, center - lower, Picture.THUMBNAIL_SIZE, center + upper)
        
        crop = resized.crop(box)
        tf = tempfile.NamedTemporaryFile('w+b')
        crop.save(tf, Picture.IMAGE_TYPE)
        self.thumbnail.save(name,File(tf), save)
        tf.close()

def _get_viewable_size(width, height):
    """
    Returns a 2-tuple of (width, height).
    
    Calculates a new width and height given a width, height.
    The larger of the width and height will be the Picture.VIEWABLE_SIZE. 
    The smaller of the two will be calculated so that the ratio is the 
    same for the new width and height.
    """
    if width > height:
        return Picture.VIEWABLE_SIZE, int(Picture.VIEWABLE_SIZE * height / width)
    else:
        return int(Picture.VIEWABLE_SIZE * width / height), Picture.VIEWABLE_SIZE

def _get_thumbnail_size(width, height):
    """
    Returns a 2-tuple of (width, height).
    
    Calculates a new width and height given a width, height.
    The smaller of the width and height will be the Picture.THUMBNAILE_SIZE. 
    The larger of the two will be calculated so that the ratio is the 
    same for the new width and height.
    """
    if width > height:
        return int(Picture.THUMBNAIL_SIZE * width / height), Picture.THUMBNAIL_SIZE
    else:
        return Picture.THUMBNAIL_SIZE, int(Picture.THUMBNAIL_SIZE * height / width)
