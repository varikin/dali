from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from dali.gallery.models import Gallery

class Page(models.Model):
    """Links to the different pages on the homepage."""
    name = models.CharField(max_length=30)
    url = models.URLField(max_length=200, blank=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True)
    image = ThumbnailerImageField(upload_to="pages")
    order = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta(object):
        ordering = ['order']


    

