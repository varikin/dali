from django.test import TestCase
from dali.gallery.models import Gallery, Picture, _get_viewable_size, _get_thumbnail_size
from dali.gallery.tests.utils import create_picture, get_image, get_temp_name

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
        pic.original = get_image(get_temp_name())
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
