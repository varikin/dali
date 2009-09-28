from datetime import datetime

from django.conf import settings
from django.contrib.comments.signals import comment_was_posted, comment_was_flagged
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

from mailer import send_mail
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
    
    def next(self):
        next = Post.objects.published().filter(date_published__gt=self.date_published).order_by('date_published')
        if next.count() > 0:
            return next[0]
        else:
            return None
    
    def previous(self):
        previous = Post.objects.published().filter(date_published__lt=self.date_published)
        if previous.count() > 0:
            return previous[0]
        else:
            return None
        

def comment_added(sender, comment, request, **kwargs):
    subject = '(%s) Comment add to: %s' % \
        (comment.site.name, comment.content_object.title)
    message = render_to_string('comments/comment_added.email', {'comment': comment})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.BLOG_AUTHOR[1]])
    
comment_was_posted.connect(comment_added)
