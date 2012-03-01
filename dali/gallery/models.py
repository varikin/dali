from django.db import models
from ckeditor.fields import HTMLField
from easy_thumbnails.fields import ThumbnailerImageField
from dali.gallery.managers import GalleryManager

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
    original = ThumbnailerImageField(upload_to='original')
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



