from collections import defaultdict
from datetime import datetime
import re
from blog.models import Post
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import simplejson as json
import posterous


class Command(BaseCommand):
    help = "Migrates posts to posterous"

    def handle(self, *args, **kwargs):
        # Figure out the full URL
        site = Site.objects.get(pk=settings.SITE_ID)
        links = re.compile(r'(src=")(/media/.*")')
        replacement = r"\1http://%s\2" % site.domain

        comments = get_comments()

        api = posterous.API(settings.POSTEROUS_USERNAME, settings.POSTEROUS_PASSWORD)
        posts = Post.objects.all()
        
        for post in posts:
            body = links.sub(replacement, post.body)
            p = api.new_post(title=post.title, body=body, date=post.date_published, autopost=False)
            print "Successfully migrated %s to %s" % (post.title, p.url) 
            post_comments = comments[post.slug]
            for comment in post_comments:
                p.new_comment(comment=comment['body'], name=comment['name'], email=comment['email'], date=comment['created_at'])
            



def get_comments():
    comments = json.load(open('comments'))
    result = defaultdict(list)
    for comment in comments:
        for c in comment:
            n = normalize_comment(c)
            result[n['slug']].append(n)
    
    for values in result.itervalues():
        values.sort(key=lambda x: x['id'])

    return result


def normalize_comment(comment):
    c = {}
    c['body'] = comment['message']
    c['id'] = comment['id']
    c['created_at'] = datetime.strptime(comment['created_at'], '%Y-%m-%dT%H:%M')
    c['url'] = comment['thread']['url']
    c['slug'] = c['url'][33:-1]
    if comment['is_anonymous']:
        author = comment['anonymous_author']
        c['name'] = author['name']
        c['email'] = author['email']
    else:
        author = comment['author']
        c['name'] = author['display_name']
        c['email'] = author['email']
    return c
        
