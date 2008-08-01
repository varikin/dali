from django.contrib import admin
from blag.models import Gallery, Picture

class GalleryAdmin(admin.ModelAdmin):
	list_display = ('name', 'webName', 'getPictureCount', 'parentGallery')
	search_fields = ('name', 'webName')

class PictureAdmin(admin.ModelAdmin):
    fields = ('name', 'webName', 'description', 'original', 'gallery', 'order')
	
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Picture, PictureAdmin)
