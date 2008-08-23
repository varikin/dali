import tempfile
import time
import unittest
import Image
from django.core.files import File
from django.core.validators import ValidationError
from dali.models import Gallery, Picture, Preferences

class PreferencesTestCase(unittest.TestCase):
    def setUp(self):
        self.pref = Preferences(thumbnail_width=100, viewable_width=1000, 
            generate_images=False)
        self.pref2 = Preferences(thumbnail_width=100, viewable_width=1000, 
            generate_images=False)
    
    def tearDown(self):
        if(self.pref.id is not None):
            self.pref.delete()
            self.pref = None
        
        if(self.pref2.id is not None):
            self.pref2.delete()
            self.pref2 = None
        
    def testCanSaveOne(self):
        self.pref.save()
        self.assert_(self.pref.id is not None)
    
    def testCannotSaveTwo(self):
        self.pref.save()
        self.assert_(self.pref.id is not None)
        self.assertRaises(ValidationError, self.pref2.save)
        
    def testCanSaveOneMultipleTimes(self):
        self.pref.save()
        self.assert_(self.pref.id is not None)
        self.pref.save()         #Should not throw an exception
        
class GalleryTestCase(unittest.TestCase):
    def setUp(self):
        self.gallery = _create_gallery()
        self.gallery.save()
        self.pref = Preferences.objects.create(thumbnail_width=100, 
            viewable_width=1000, generate_images=False)
    
    def tearDown(self):
        self.gallery.delete()
        self.gallery = None
        self.pref.delete()
        self.pref = None        
         
    def testRandomNoPictures(self):
        picture = self.gallery.getRandomPicture()
        self.assert_(picture is None)
    
    def testRandomWithPictures(self):
        expected = _create_picture(self.gallery)
        expected.save()
        actual = self.gallery.getRandomPicture()
        self.assertEquals(expected, actual)
        
    def testCountNoPictures(self):
        count = self.gallery.getPictureCount()
        self.assertEquals(0, count)
        
    def testCountWithPictures(self):
        expected = 4
        for i in range(expected):
            _create_picture(self.gallery).save()
        actual = self.gallery.getPictureCount()
        self.assertEquals(expected, actual)
  
class PictureTestCase(unittest.TestCase):
    def setUp(self):
        self.gallery = _create_gallery()
        self.gallery.save()
        self.picture = _create_picture(self.gallery)
        self.pref = Preferences.objects.create(thumbnail_width=100, 
            viewable_width=1000, generate_images=False)
         
    def tearDown(self):
        if(self.picture.id is not None):
            self.picture.delete()
        self.picture = None
        self.gallery.delete()
        self.gallery = None
        self.pref.delete()
        self.pref = None
        
    def testGenerateOnFirstSave(self):
        generated = self.picture.save()
        self.assert_(generated)

    def testPreferenceFalse(self):
        generated = self.picture.save()
        self.assert_(generated)
        generated = self.picture.save()
        self.failIf(generated)
    
    def testPreferenceTrue(self):
        self.pref.generate_images = True
        self.pref.save()
        generated = self.picture.save()
        self.assert_(generated)
        generated = self.picture.save()
        self.assert_(generated)

def _create_picture(gallery):
    """
    Return a Picture that is not saved.
    """
    name = _get_unique_string()
    pic = Picture(name=name, webName=name, gallery=gallery)
    pic.original.save(''.join([pic.name,'.jpg']), File(_get_temp_image()), False)
    return pic
    
def _create_gallery():
    """
    Return a Gallery that is not saved.
    """
    name = _get_unique_string()
    return Gallery(name=name, webName=name)
   
def _delete_object(object):
     if(object is not None):
         object.delete()
         object = None
    
def _get_unique_string():
    """
    Return unique string for use as name in tests.
    """
    return 'test_' + str(time.time())
            
def _get_temp_image():
    """
    Return a temporary file that contains in image.  The file will be 
    automatically deleted when closed.
    """
    tf = tempfile.NamedTemporaryFile()
    im = Image.new('RGB', (100,100))
    im.save(tf, 'JPEG')
    return tf
        
        