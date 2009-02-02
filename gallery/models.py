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
    parentGallery = models.ForeignKey('self', null=True, blank=True)
    published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    objects = GalleryManager()
    verbose_name_plural = "galleries"
    ordering = ('date_created',)
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
        # Determine if this is a new picture object or new original file.
         
        generate_images = True
        if self.id is not None:
            old_picture = Picture.objects.get(pk=self.id)
            if self.original.path == old_picture.original.path:
                generate_images = False
        
        if generate_images:
            orig = Image.open(self.original.path)
            name = os.path.basename(self.original.name)
            self.create_viewable(orig, name)
            self.create_thumbnail(orig, name)
        
        super(Picture, self).save(**kwargs)    
        return generate_images
        
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
        
        width, height = self._get_size(image.size[0], image.size[1], 
            Picture.VIEWABLE_SIZE)
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

        landscape = image.size[0] > image.size[1]
        lower, remainder = divmod(Picture.THUMBNAIL_SIZE, 2)
        upper = lower
        if remainder != 0: 
            upper += 1        

        if landscape:
            height, width = self._get_size(image.size[1], image.size[0], 
                Picture.THUMBNAIL_SIZE)
            resized = image.resize((width, height), Image.ANTIALIAS)        
            center = resized.size[0] // 2
            box = (center - lower, 0, center + upper, Picture.THUMBNAIL_SIZE)
        else:
            width, height = self._get_size(image.size[0], image.size[1], 
                Picture.THUMBNAIL_SIZE)
            resized = image.resize((width, height), Image.ANTIALIAS)        
            center = resized.size[1] // 2
            box = (0, center - lower, Picture.THUMBNAIL_SIZE, center + upper)
        
        crop = resized.crop(box)
        tf = tempfile.NamedTemporaryFile('w+b')
        crop.save(tf, Picture.IMAGE_TYPE)
        self.thumbnail.save(name,File(tf), save)
        tf.close()
        
    def _get_size(self, short, long_, const):
        return const, int(const * long_ / short)
