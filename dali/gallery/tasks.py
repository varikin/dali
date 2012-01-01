from __future__ import division

import tempfile
from PIL import Image
from celery.registry import tasks
from celery.task import Task
from django.core.files.base import File
import os
from gallery.models import Picture
from django.conf import settings

class GenerateImages(Task):

    def run(self, id):
        """Generates a viewable and thumbnail fo an image."""
        try:
            self.picture = Picture.objects.get(pk=id)
        except Picture.DoesNotExist, dne:
            #TODO: handle this
            return

        name = os.path.basename(self.picture.original.name)

        try:
            orig = Image.open(self.picture.original.path)
            orig.verify() # Need to reload image after verifying
        except:
            #TODO: deal with failure
            return

        orig = Image.open(self.picture.original.path)
        self.create_viewable(orig, name)
        self.create_thumbnail(orig, name)

        self.picture.save()

    def create_viewable(self, image, name):
        """
        Creates a viewable for a Picture.

        image: A PIL image.  If not given, opens the original with PIL.
        name: A name for the viewable.  If not given, uses base name of the
            original
        """
        width, height = _get_size(settings.GALLERY_VIEWABLE_SIZE, image)
        resized = image.resize((width, height), Image.ANTIALIAS)
        tf = tempfile.NamedTemporaryFile()
        resized.save(tf, settings.GALLERY_IMAGE_TYPE)
        self.picture.viewable.save(name, File(tf), False)
        tf.close()

    def create_thumbnail(self, image, name):
        """
        Creates a thumbnail for a Picture.

        The thumbnail is cropped to be square.
        picture: A Picture object
        image: A PIL image.  If not given, opens the original with PIL.
        name: A name for the viewable.  If not given, uses basename of the
            original
        """
        width, height = _get_size(settings.GALLERY_THUMBNAIL_SIZE, image)
        resized = image.resize((width, height), Image.ANTIALIAS)

        lower, remainder = divmod(settings.GALLERY_THUMBNAIL_SIZE, 2)
        upper = lower
        if remainder:
            upper += 1

        if width > height:
            center = resized.size[0] // 2
            box = (center - lower, 0, center + upper, settings.GALLERY_THUMBNAIL_SIZE)
        else:
            center = resized.size[1] // 2
            box = (0, center - lower, settings.GALLERY_THUMBNAIL_SIZE, center + upper)

        crop = resized.crop(box)
        tf = tempfile.NamedTemporaryFile()
        crop.save(tf, settings.GALLERY_IMAGE_TYPE)
        self.picture.thumbnail.save(name, File(tf), False)
        tf.close()


tasks.register(GenerateImages)




def _get_size(max_size, image):
    """
    Returns a 2-tuple of (width, height).

    Calculates a new width and height given a width, height.
    The larger of the width and height will be the max_size
    The smaller of the two will be calculated so that the ratio is the
    same for the new width and height.
    """
    width = image.size[0]
    height = image.size[1]
    if width > height:
        return max_size, int(max_size * height / width)
    else:
        return int(max_size * width / height), max_size
