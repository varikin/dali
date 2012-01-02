from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest, QueryDict
from django.test import TestCase
from django.test.client import Client
from dali.gallery.admin.forms import ZipFileForm, _normalize_name, _unique_slug
from dali.gallery.models import Gallery, Picture
from dali.gallery.tests.utils import add_permission, create_picture

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

class UploadZipFileTestCase(TestCase):
    fixtures = ['gallery.json', 'user.json']

    def setUp(self):
        self.user = User.objects.get(username='test')
        self.perm = Permission.objects.filter(content_type__name='picture')
        self.url = '/gallery/picture/add_from_zip/'
        self.redirect = '/admin/gallery/picture/'
        self.gallery = Gallery.objects.get(slug='TestGallery')
        self.path = 'gallery/tests/example'
        
    def test_not_logged_in(self):
        f = file('%s/valid_images.zip' % self.path)
        data = {u'gallery': self.gallery.id, u'zip_file': f}
        self.client.post(self.url, data)
        f.close()
        pictures = Picture.objects.filter(gallery=self.gallery.id)
        self.assertEquals(0, len(pictures))

    def test_logged_in_no_permission(self):
        self.client.login(username='test', password='test')
        f = file('%s/valid_images.zip' % self.path)
        data = {u'gallery': self.gallery.id, u'zip_file': f}
        self.client.post(self.url, data)
        f.close()
        pictures = Picture.objects.filter(gallery=self.gallery.id)
        self.assertEquals(0, len(pictures))

    def test_all_valid_images(self):
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        f = file('%s/valid_images.zip' % self.path)
        data = {u'gallery': self.gallery.id, u'zip_file': f}
        response = self.client.post(self.url, data)
        f.close()
        pictures = Picture.objects.filter(gallery=self.gallery.id)
        self.assertEquals(2, len(pictures))
        self.assertRedirects(response, self.redirect)

    def test_all_invalid_images(self):
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        f = file('%s/invalid_images.zip' % self.path)
        data = {u'gallery': self.gallery.id, u'zip_file': f}
        response = self.client.post(self.url, data)
        f.close()
        pictures = Picture.objects.filter(gallery=self.gallery.id)
        self.assertEquals(0, len(pictures))
        self.assertRedirects(response, self.redirect)

    def test_valid_invalid_mix(self):
        add_permission(self.user, self.perm)
        self.client.login(username='test', password='test')
        f = file('%s/mixed_images.zip' % self.path)
        data = {u'gallery': self.gallery.id, u'zip_file': f}
        response = self.client.post(self.url, data)
        f.close()
        pictures = Picture.objects.filter(gallery=self.gallery.id)
        self.assertEquals(2, len(pictures))
        self.assertRedirects(response, self.redirect)
        
class NormalizeNameTestCase(TestCase):
    
    def setUp(self):
        self.normalized = 'Awesome Picture'
    
    def test_no_changes(self):
        self.assertEquals(self.normalized, _normalize_name(self.normalized))

    def test_remove_extension(self):
        name = '%s.jpg' % self.normalized
        self.assertEquals(self.normalized, _normalize_name(name))

    def test_remove_multiple_extensions(self):
        name = '%s.jpg.jpg' % self.normalized
        self.assertEquals(self.normalized, _normalize_name(name))

    def test_remove_leading_path(self):
        name = 'some/path/%s' % self.normalized
        self.assertEquals(self.normalized, _normalize_name(name))

    def test_replace_underscores(self):
        name = 'Awesome_Picture'
        self.assertEquals(self.normalized, _normalize_name(name))

    def test_extensions_paths_underscores(self):
        name = '/some/path/Awesome_Picture.jpg.jpg'
        self.assertEquals(self.normalized, _normalize_name(name))
