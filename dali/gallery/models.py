from __future__ import division
import os
import tempfile
from PIL import Image
from ckeditor.fields import HTMLField

from django.core.files import File
from django.db import models

from gallery.managers import GalleryManager

class Gallery(models.Model):    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = HTMLField(null=True, blank=True)
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
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    original = models.ImageField(upload_to='original')
    viewable = models.ImageField(upload_to='viewable')
    thumbnail = models.ImageField(upload_to='thumbnail')
    description = HTMLField(null=True, blank=True)
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
        
        # Generate images if new Picture or change original file
        if old_path is None or self.original.path != old_path:
            name = os.path.basename(self.original.name)

            # Save before generating image
            # The uploaded images are not avalable till after saving
            super(Picture, self).save(**kwargs)
            try:
                orig = Image.open(self.original.path)
                orig.verify() # Need to reload image after verifying
            except:
                # Treating errors to mean a bad image file. If new Picture,
                # delete the Picture. Else, set original to the old original
                # Then re-raise the exception
                if old_path is None:
                    self.delete()
                else:
                    self.original.save(self.name,File(file(old_path)), save=True)
                raise

            orig = Image.open(self.original.path)
            self.create_viewable(orig, name)
            self.create_thumbnail(orig, name)

        # Lets see how many times we can save this fucking image
        super(Picture, self).save(**kwargs)