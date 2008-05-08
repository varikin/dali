from django.db import models
import os

# Create your models here.
class Folder(models.Model):
	name = models.CharField(max_length = 200)
	#folder path is relative to the parent.  If root, absolute
	path = models.CharField(max_length = 200)
	parentFolder = models.ForeignKey('self', db_column = 'parent_folder', null=True)
	webEnabled = models.BooleanField(default = False)
	
	def __unicode__(self):
		return self.name
		
	def getPath(self):
		current = self
		path = current.path
		while not current.isRoot():
			current = current.parentFolder
			path = current.path + os.sep + path
		return path
		
	def getUrl(self):
		current = self
		webSep = "/"
		path = current.path
		while not current.isRoot():
			current = current.parentFolder
			if not current.webEnabled:
				break
			path = current.path + webSep + path
		return path
		
	def isRoot(self):
		result = False
		if self.parentFolder is None:
			result = True
		return result
		
		
class Media(models.Model):
	name = models.CharField(max_length = 200)
	folder = models.ForeignKey(Folder)
	
	def __unicode__(self):
		return self.name
		
	def getPath(self):
		return self.folder.getPath() + os.sep + self.name
		
	def getUrl(self):
		webSep = "/"
		return webSep + self.folder.getUrl() + webSep + self.name
		

		
class Gallery(models.Model):
	name = models.CharField(max_length = 200)
	description = models.TextField()
	parentGallery = models.ForeignKey('self', null=True)
	
	def __unicode__(self):
		return self.name

class Image(models.Model):
	name = models.CharField(max_length = 200)
	original = models.ForeignKey(Media, related_name = "original")
	viewable = models.ForeignKey(Media, related_name = "viewable")
	thumbnail = models.ForeignKey(Media, related_name = "thumbnail")
	description = models.TextField()
	gallery = models.ForeignKey(Gallery)
	order = models.PositiveSmallIntegerField()
	
	def __unicode__(self):
		return self.name
	
	
class Link(models.Model):
	url = models.URLField(max_length = 200, verify_exists = False)
	text = models.CharField(max_length = 200)
	
	def __unicode__(self):
		return self.text
	
	
class LinkList(models.Model):
	name = models.CharField(max_length = 200)
	links = models.ManyToManyField(Link)
	
	def __unicode__(self):
		return self.name
	
	
class Tag(models.Model):
	name = models.CharField(max_length = 200)
	
	def __unicode__(self):
		return self.name
	
	
class Post(models.Model):
	title = models.CharField(max_length = 200)
	content = models.TextField()
	tags = models.ManyToManyField(Tag)
	author = models.CharField(max_length = 200)
	created = models.DateTimeField(auto_now_add = True)
	modified = models.DateTimeField(auto_now = True)
	
	def __unicode__(self):
		return self.title
	