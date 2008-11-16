from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

class CustomFlatPageAdmin(FlatPageAdmin):
    class Media:
            js = (
                '/static/js/tiny_mce/tiny_mce.js',
                '/static/js/tiny_init.js',
            )

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)

