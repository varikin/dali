import tempfile
from PIL import Image
from celery.task import Task
import os
from gallery.models import Picture
from django.conf import settings

@Task
def generate_images(self, id):
    """Generates a viewable and thumbnail fo an image."""
    try:
        picture = Picture.objects.get(pk=id)
    except Picture.DoesNotExist, dne:
        #TODO: handle this
        return

    name = os.path.basename(picture.original.name)

    try:
        orig = Image.open(picture.original.path)
        orig.verify() # Need to reload image after verifying
    except:
        #TODO: deal with failure
        return

    orig = Image.open(picture.original.path)
    self.create_viewable(orig, name)
    self.create_thumbnail(orig, name)

    picture.save()

def create_viewable(picture, image, name, save=False):
    """
    Creates a viewable for a Picture.

    picture: A Picture object
    image: A PIL image.  If not given, opens the original with PIL.
    name: A name for the viewable.  If not given, uses base name of the
        original
    save: Whether to save the object or not.
    """
    width, height = _get_size(settings.GALLERY_VIEWABLE_SIZE, image)
    resized = image.resize((width, height), Image.ANTIALIAS)
    tf = tempfile.NamedTemporaryFile()
    resized.save(tf, settings.GALLERY_IMAGE_TYPE)
    picture.viewable.save(name, File(tf), save)
    tf.close()

def create_thumbnail(picture, image, name, save=False):
    """
    Creates a thumbnail for a Picture.

    The thumbnail is cropped to be square.
    picture: A Picture object
    image: A PIL image.  If not given, opens the original with PIL.
    name: A name for the viewable.  If not given, uses basename of the
        original
    save: Whether to save the object or not.
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
    picture.thumbnail.save(name, File(tf), save)
    tf.close()

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
