from django.contrib import admin
from dali.gallery.models import Gallery, Picture

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'picture_count', 'parent_gallery',
        'date_created', 'date_modified', 'published')
    list_editable = ('slug', 'order', 'parent_gallery', 'published')
    save_on_top = True
    list_filter = ('date_created', 'date_modified')
    search_fields = ('name', 'slug', 'parent_gallery__name')
    prepopulated_fields = {'slug': ('name',)}

class PictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'gallery', 'order', 
        'date_created', 'date_modified')
    list_editable = ('slug', 'gallery', 'order')
    search_fields = ('name', 'original', 'gallery__name')
    save_on_top = True
    list_filter = ('gallery', 'date_created', 'date_modified')
    fields = ('name', 'slug', 'description', 'original', 'gallery', 'order')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Picture, PictureAdmin)
