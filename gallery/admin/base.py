from django.contrib import admin
from gallery.models import Gallery, Picture

class GalleryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'picture_count', 'parentGallery', 
        'date_created', 'date_modified', 'published')
	list_filter = ('date_created', 'date_modified')
	search_fields = ('name', 'slug')
	prepopulated_fields = {'slug': ('name',)}

class PictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'gallery', 'order', 
        'date_created', 'date_modified')
    search_fields = ('name', 'original', 'gallery')
    list_filter = ('gallery', 'date_created', 'date_modified')
    fields = ('name', 'slug', 'description', 'original', 'gallery', 'order')
    prepopulated_fields = {'slug': ('name',)}
        
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Picture, PictureAdmin)
