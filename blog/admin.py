from django.contrib import admin
from django import forms
from blog.models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'date_published', 'published')
	list_filter = ('date_published', 'published')
	search_fields = ('title', 'raw_body')
	prepopulated_fields = {'slug': ('title',)}
	
	fieldsets = (
	    ('Title', {'fields': (('title', 'slug'),)}), 
	    ('Post', {'fields': ('body',)}),
	    ('Tags', {'fields': ('tags',)}),
	    ('Extra', {'fields': ('published', 'date_published',)}),
	)
	
	class Media:
	    js = (
	        '/static/js/tiny_mce/tiny_mce.js',
	        '/static/js/tiny_init.js',
	    )

admin.site.register(Post, PostAdmin)
