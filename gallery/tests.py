import random
import Image
from StringIO import StringIO
from django.contrib.auth.models import User, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import Client
from gallery.models import Gallery, Picture, _get_size
from gallery.admin.views import save_picture_order
        
class GalleryTestCase(TestCase):
    fixtures = ['gallery.json']
        
    def setUp(self):
        self.gallery = Gallery.objects.get(slug='TestGallery') 
        
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
        self.gallery = Gallery.objects.get(slug='TestGallery')
        self.picture = create_picture(self.gallery)
        
    def test_generate_on_new_picture(self):
        self.assert_(self.picture.save())

    def test_no_generate_on_save(self):
        self.assert_(self.picture.save())
        self.failIf(self.picture.save())
    
    def test_generate_on_save_with_new_image(self):
        pic = self.picture
        self.assert_(pic.save())
        pic.original = _get_image(_get_temp_name())
        self.assert_(pic.save())
    
    def test_get_size_landscape(self):
        w, h = _get_size(1000, 800, 400)
        self.assertEquals(320, h, 'The height is not correct')
        self.assertEquals(400, w, 'The width is not correct')
        
    def test_get_size_portrait(self):
        w, h = _get_size(800, 1000, 400)
        self.assertEquals(400, h, 'The height is not correct')
        self.assertEquals(320, w, 'The width is not correct')
        
    def test_get_size_square(self):
        w, h = _get_size(832, 832, 400)
        self.assertEquals(w, h, 'The width is not equal to the height')
        self.assertEquals(400, w, 'The width is not target size')

class SaveOrderTestCase(TestCase):
    fixtures = ['gallery.json', 'pictures.json', 'user.json']
    
    def setUp(self):
        self.user = User.objects.get(username='test')
        self.perm = Permission.objects.get(codename='change_picture')
        self.url = '/gallery/picture/save_order/'
                    
    def test_not_logged_in(self):
        picture = Picture.objects.get(slug='TestPicture1')
        data = {unicode(picture.id): u'3'}
        self.client.post(self.url, data)
        picture = Picture.objects.get(slug='TestPicture1')
        self.failIf(picture.order)
    
    def test_logged_in_not_ajax(self):
        picture = Picture.objects.get(slug='TestPicture1')
        data = {unicode(picture.id): u'3'}
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        self.client.post(self.url, data)
        picture = Picture.objects.get(slug='TestPicture1')
        self.failIf(picture.order)
        
    def test_logged_in_no_permission(self):
        picture = Picture.objects.get(slug='TestPicture1')
        data = {unicode(picture.id): u'3'}
        self.client.login(username='test', password='test')
        self.client.post(self.url, data, **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        picture = Picture.objects.get(slug='TestPicture1')
        self.failIf(picture.order)
        
    def test_logged_in_is_ajax(self):
        picture = Picture.objects.get(slug='TestPicture1')
        data = {unicode(picture.id): u'3'}
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        self.client.post(self.url, data, **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        picture = Picture.objects.get(slug='TestPicture1')
        self.assertEquals(3, picture.order)
        
    def test_get_method(self):
        picture = Picture.objects.get(slug='TestPicture1')
        data = {unicode(picture.id): u'3'}
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        self.client.get(self.url, data, **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
        picture = Picture.objects.get(slug='TestPicture1')
        self.failIf(picture.order)

def add_permission(user, perm):
    """Add a permission to a user."""
    user.user_permissions.add(perm)
    user.save()

def create_picture(gallery, width=100, height=100):
    """Return a Picture that is not saved."""
    name = _get_temp_name()
    pic = Picture(name=name, slug=name, gallery=gallery)
    pic.original = _get_image(name, width, height)
    return pic

def _get_temp_name():
    return "test_%d" % random.randint(1,10000000)

def _get_image(name, width=100, height=100):
    """
    Return an image.
    """
    f = StringIO()
    im = Image.new('RGB', (width, height))
    im.save(f, 'JPEG')    
    return SimpleUploadedFile(name + '.jpg', f.getvalue())
