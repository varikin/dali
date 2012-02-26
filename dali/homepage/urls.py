from django.conf.urls.defaults import *
from django.views.generic.list import ListView

from dali.homepage.models import Page

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Page), name="homepage")
)