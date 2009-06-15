import random
import Image
from StringIO import StringIO
from django.contrib.auth.models import User, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.http import HttpRequest, QueryDict
from django.test import TestCase
from django.test.client import Client
from gallery.models import Gallery, Picture, _get_viewable_size, _get_thumbnail_size
from gallery.admin.forms import ZipFileForm, _unique_slug

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

    def test_get_viewable_size_landscape(self):
        w, h = _get_viewable_size(1000, 800)
        self.assertEquals(320, h, 'The height is not correct')
        self.assertEquals(400, w, 'The width is not correct')

    def test_get_viewable_size_portrait(self):
        w, h = _get_viewable_size(800, 1000)
        self.assertEquals(400, h, 'The height is not correct')
        self.assertEquals(320, w, 'The width is not correct')

    def test_get_viewable_size_square(self):
        w, h = _get_viewable_size(832, 832)
        self.assertEquals(w, h, 'The width is not equal to the height')

    def test_get_thumbnail_size_landscape(self):
        w, h = _get_thumbnail_size(1000, 800)
        self.assertEquals(75, h, 'The height is not correct')
        self.assertEquals(93, w, 'The width is not correct')

    def test_get_thumbnail_size_portrait(self):
        w, h = _get_thumbnail_size(800, 1000)
        self.assertEquals(93, h, 'The height is not correct')
        self.assertEquals(75, w, 'The width is not correct')

    def test_get_thumbnail_size_square(self):
        w, h = _get_thumbnail_size(1232, 1232)
        self.assertEquals(w, h, 'The width is not equal to the height')

class UniqueSlugTestCase(TestCase):
    fixtures = ['gallery.json']

    def setUp(self):
        self.gallery = Gallery.objects.get(slug='TestGallery')

    def test_unique_slug_no_conflicts(self):
        self.assertEquals("slug", _unique_slug("slug"), "The slug should no be altered.")

    def test_unique_slug_one_conflict(self):
        create_picture(self.gallery, "slug").save()
        self.assertEquals("slug-1", _unique_slug("slug"), "The slug should be incremented.")

    def test_unique_slug_multiple_conflicts(self):
        create_picture(self.gallery, "slug").save()
        create_picture(self.gallery, "slug-1").save()
        create_picture(self.gallery, "slug-2").save()
        self.assertEquals("slug-3", _unique_slug("slug"), "The slug should be incremented.")

class CleanZipFileTestCase(TestCase):
    fixtures = ['gallery.json']

    def setUp(self):
        self.zip_error = { u'zip_file': [u'A zip file is required:)'] }

    def test_invalid_file_extension(self):
        form = self.get_form('a_file.txt', 'applciation/zip')
        self.assertEquals(self.zip_error, form.errors)

    def test_invalid_content_type_text(self):
        form = self.get_form('a_file.zip', 'text/plain')
        self.assertEquals(self.zip_error, form.errors, 'Should not allow text/plain content type.')

    def test_invalid_content_type_html(self):
        form = self.get_form('a_file.zip', 'text/html')
        self.assertEquals(self.zip_error, form.errors, 'Should not allow text/html content type.')

    def test_invalid_content_type_binary(self):
        form = self.get_form('a_file.zip', 'application/octet-stream')
        self.assertEquals(self.zip_error, form.errors, 'Should not allow application/octet-stream content type.')

    def test_invalid_content_type_jpeg(self):
        form = self.get_form('a_file.zip', 'image/jpeg')
        self.assertEquals(self.zip_error, form.errors, 'Should not allow image/jpeg content type.')

    def test_valid_file_application_zip(self):
        form = self.get_form('test.zip', 'application/zip')
        self.assertEquals({}, form.errors)

    def test_valid_file_application_x_zip(self):
        form = self.get_form('test.zip', 'application/x-zip')
        self.assertEquals({}, form.errors)

    def test_valid_file_application_x_zip_compressed(self):
        form = self.get_form('test.zip', 'application/x-zip-compressed')
        self.assertEquals({}, form.errors)

    def test_valid_file_application_x_compress(self):
        form = self.get_form('test.zip', 'application/x-compress')
        self.assertEquals({}, form.errors)

    def test_valid_file_application_x_compressed(self):
        form = self.get_form('test.zip', 'application/x-compressed')
        self.assertEquals({}, form.errors)

    def test_valid_file_application_multipart_x_zip(self):
        form = self.get_form('test.zip', 'multipart/x-zip')
        self.assertEquals({}, form.errors)

    def get_form(self, filename, content_type):
        request = HttpRequest()
        request.POST = QueryDict('gallery=1')
        request.FILES = {  u'zip_file': SimpleUploadedFile(filename, 'content', content_type) }
        return ZipFileForm(request.POST, request.FILES)

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

def create_picture(gallery, name=None, width=100, height=100):
    """Return a Picture that is not saved."""
    name = name or _get_temp_name()
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
