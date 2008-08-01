import os
import Image
from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile

class Gallery(models.Model):
    name = models.CharField(max_length=200)
    webName = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    parentGallery = models.ForeignKey('self', null=True, blank=True)
        
    def __unicode__(self):
        return self.name
    
    def getRandomPicture(self):
        try:
            picture = Picture.objects.filter(gallery = self).order_by('?')[0:1].get()
        except Picture.DoesNotExist:
            picture = None
        
        return picture
    
    def getPictureCount(self):
        """
        Returns the number of pictures in the gallery; return an integer
        """
        count = Picture.objects.filter(gallery = self).count()
        return count
    
    getPictureCount.short_description = 'Number of Pictures'

class Picture(models.Model):
    name = models.CharField(max_length=200)
    webName = models.CharField(max_length=200, unique=True)
    original = models.ImageField(upload_to="original")
    viewable = models.ImageField(upload_to="viewable")
    thumbnail = models.ImageField(upload_to="thumbnail")
    description = models.TextField()
    gallery = models.ForeignKey(Gallery)
    order = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return self.name
