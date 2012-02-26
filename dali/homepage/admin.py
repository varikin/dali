from django.contrib import admin
from dali.homepage.models import Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'gallery', 'url', 'order')
    save_on_top = True

admin.site.register(Page, PageAdmin)