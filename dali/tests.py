import random
import tempfile
import unittest
import Image
from django.contrib.auth.models import User, Permission
from django.core.files import File
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
from dali.models import Gallery, Picture, Preferences
from dali.admin.views import save_picture_order

class PreferencesTestCase(TestCase):
    def test_cannot_save_two(self):
        """Can save one is taken care of by initial_data.json fixture:)"""
        pref = Preferences(thumbnail_width=100, viewable_width=1000,
            generate_images=False, image_type='JPEG')
        self.assertRaises(ValidationError, pref.save)
        
    def test_can_save_one_multiple_times(self):
        pref = Preferences.objects.get_preference() 
        pref.save()         #Should not throw an exception
        
class GalleryTestCase(TestCase):
    fixtures = ['gallery.json']
        
    def setUp(self):
        self.gallery = Gallery.objects.get(web_name='TestGallery') 
         
    def test_random_no_pictures(self):
        picture = self.gallery.random_picture()
        self.assert_(picture is None)
    
    def test_random_with_pictures(self):
        expected = create_picture(self.gallery)
        expected.save()
        actual = self.gallery.random_picture()
        self.assertEquals(expected, actual)
        
    def test_count_no_pictures(self):
        count = self.gallery.picture_count()
        self.assertEquals(0, count)
        
    def test_count_with_pictures(self):
        expected = 4
        for i in range(expected):
            create_picture(self.gallery).save()
        actual = self.gallery.picture_count()
        self.assertEquals(expected, actual)
  
class PictureTestCase(TestCase):
    fixtures = ['gallery.json']
    
    def setUp(self):
        gallery = Gallery.objects.get(web_name='TestGallery')
        self.picture = create_picture(gallery)
        
    def test_generate_on_first_save(self):
        self.assert_(self.picture.save())

    def test_preference_false(self):
        self.assert_(self.picture.save())
        self.failIf(self.picture.save())
    
    def test_preference_true(self):
        pref = Preferences.objects.get_preference()
        pref.generate_images = True
        pref.save()
        self.assert_(self.picture.save())
        self.assert_(self.picture.save())

class SaveOrderTestCase(TestCase):
    fixtures = ['gallery.json', 'pictures.json', 'user.json']
    
    def setUp(self):
        self.user = User.objects.get(username='test')
        self.perm = Permission.objects.get(codename='change_picture')
        self.url = '/dali/picture/save_order/'
                    
    def test_not_logged_in(self):
        picture = Picture.objects.get(web_name='TestPicture1')
        data = {unicode(picture.id): u'3'}
        self.client.post(self.url, data)
        picture = Picture.objects.get(web_name='TestPicture1')
        self.failIf(picture.order)
    
    def test_logged_in_not_ajax(self):
        picture = Picture.objects.get(web_name='TestPicture1')
        data = {unicode(picture.id): u'3'}
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        self.client.post(self.url, data)
        picture = Picture.objects.get(web_name='TestPicture1')
        self.failIf(picture.order)
        
    def test_logged_in_no_permission(self):
        picture = Picture.objects.get(web_name='TestPicture1')
        data = {unicode(picture.id): u'3'}
        self.client.login(username='test', password='test')
        self.client.post(self.url, data, **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        picture = Picture.objects.get(web_name='TestPicture1')
        self.failIf(picture.order)
        
    def test_logged_in_is_ajax(self):
        picture = Picture.objects.get(web_name='TestPicture1')
        data = {unicode(picture.id): u'3'}
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        self.client.post(self.url, data, **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        picture = Picture.objects.get(web_name='TestPicture1')
        self.assertEquals(3, picture.order)
        
    def test_get_method(self):
        picture = Picture.objects.get(web_name='TestPicture1')
        data = {unicode(picture.id): u'3'}
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        self.client.get(self.url, data, **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        picture = Picture.objects.get(web_name='TestPicture1')
        self.failIf(picture.order)

def add_permission(user, perm):
    """Add a permission to a user."""
    user.user_permissions.add(perm)
    user.save()

def create_picture(gallery):
    """Return a Picture that is not saved."""
    name = "temp_%d" % random.randint(1,10000000)
    pic = Picture(name=name, web_name=name, gallery=gallery)
    pic.original.save(''.join([pic.name,'.jpg']), File(_get_temp_image()), False)
    return pic
            
def _get_temp_image():
    """
    Return a temporary file that contains in image.  The file will be 
    automatically deleted when closed.
    """
    tf = tempfile.NamedTemporaryFile()
    im = Image.new('RGB', (100,100))
    im.save(tf, 'JPEG')
    return tf
