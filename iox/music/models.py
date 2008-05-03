from django.db import models

class Song(models.Model):
	name = models.CharField(max_length = 200)
	artist = models.CharField(max_length = 200)
	album = models.CharField(max_length = 200)
	play_count = models.PositiveIntegerField(blank = True, null = True)
	last_played = models.DateTimeField(blank = True, null = True)
	rating = models.PositiveIntegerField(blank = True, null = True)
	songs_played_after = models.ManyToManyField('self', blank = True, null = True)
	#songs_played_before = models.ManyToManyField(Song)
	filename = models.FileField(upload_to = 'music/songs', blank = True, null = True)
	
	def __unicode__(self):
		return self.name
	
	def valid_sound_file(self, filename):
		return is_mp3(filename) or is_ogg(filename)
		
	def is_mp3(self, filename):
		return filename.endswith("mp3")	
		
	def is_ogg(self, filename):
		return filename.endswith("ogg")
	
	class Admin:
		pass
	
class Playlist(models.Model):
	name = models.CharField(max_length = 200)
	songs = models.ManyToManyField(Song)
	
	def __unicode__(self):
		return self.name

#	class Admin:
#		pass
