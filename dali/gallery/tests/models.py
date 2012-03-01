from django.test import TestCase
from dali.gallery.models import Gallery
from dali.gallery.tests.utils import create_picture

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

