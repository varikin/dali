from django.contrib import admin
from dali.models import Gallery, Picture, Preferences

class GalleryAdmin(admin.ModelAdmin):
	list_display = ('name', 'webName', 'getPictureCount', 'parentGallery', 'published')
	search_fields = ('name', 'webName')


class PictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'webName', 'description', 'gallery', 'order')
    search_fields = ('name', 'original', 'gallery')
    list_filter = ('gallery', )
    fields = ('name', 'webName', 'description', 'original', 'gallery', 'order')
    
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Preferences)
