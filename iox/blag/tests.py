import unittest
from iox.blag.models import *

class FolderTestCase(unittest.TestCase):
	
	def setUp(self):
		self.foo = Folder(name = "foo", path = "/foo")
		self.bar = Folder(name = "bar", path = "bar")
		self.foo.save()
		self.bar.parentFolder = self.foo
		self.bar.save()
		
	
	def test_isRoot_RootNotSet(self):
		self.assert_(self.foo.isRoot())
	
	def test_isRoot_NotRoot(self):
		self.assert_(not self.bar.isRoot())
		
	def test_getPath_RootPath(self):
		self.assertEquals(self.foo.getPath(), "/foo")
		
	def test_getPath_TwoLevelPath(self):
		self.assertEquals(self.bar.getPath(), "/foo/bar")
		
	def test_getPath_ThreeLevelPath(self):
		f = Folder(name = "folder", path = "folder")
		f.parentFolder = self.bar
		f.save()
		self.assertEquals(f.getPath(), "/foo/bar/folder")

class MediaTestCase(unittest.TestCase):
	
	def setUp(self):
		self.foo = Folder(name = "foo", path = "/foo")
		self.bar = Folder(name = "bar", path = "bar")
		self.foo.save()
		self.bar.parentFolder = self.foo
		self.bar.save()
		self.image = Media(name = "image")
	
	def test_getPath_RootFolder(self):
		self.image.folder = self.foo
		self.image.save()
		self.assertEquals(self.image.getPath(), "/foo/image")
		
	def test_getPath_NotRootFolder(self):
		self.image.folder = self.bar
		self.image.save()
		self.assertEquals(self.image.getPath(), "/foo/bar/image")
		
		
		
		
	