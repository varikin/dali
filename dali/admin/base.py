from django.contrib import admin
from dali.models import Gallery, Picture, Preferences

class GalleryAdmin(admin.ModelAdmin):
	list_display = ('name', 'web_name', 'picture_count', 'parentGallery', 
        'date_created', 'date_modified', 'published')
	list_filter = ('date_created', 'date_modified')
	search_fields = ('name', 'web_name')

class PictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'web_name', 'gallery', 'order', 
        'date_created', 'date_modified')
    search_fields = ('name', 'original', 'gallery')
    list_filter = ('gallery', 'date_created', 'date_modified')
    fields = ('name', 'web_name', 'description', 'original', 'gallery', 'order')
    
    class Media:
        js = ("js/jquery.js", "js/jquery.ui/ui.core.js", "js/jquery.ui/ui.sortable.js", "js/sort.js")
    
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Preferences)
