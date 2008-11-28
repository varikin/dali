from datetime import datetime
from django.db import models
from tagging.fields import TagField
from blog.managers import PostManager

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    published= models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(default=datetime.now)
    tags = TagField()
    
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ("-date_published",)
    
    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_detail", (), {"slug": self.slug})