import random
import Image
from StringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from gallery.models import Picture

def add_permission(user, perm):
    """Add a permission to a user."""
    user.user_permissions.add(perm)
    user.save()

def create_picture(gallery, name=None, width=100, height=100):
    """Return a Picture that is not saved."""
    name = name or get_temp_name()
    pic = Picture(name=name, slug=name, gallery=gallery)
    pic.original = get_image(name, width, height)
    return pic

def get_image(name, width=100, height=100):
    """Return an image."""
    f = StringIO()
    im = Image.new('RGB', (width, height))
    im.save(f, 'JPEG')    
    return SimpleUploadedFile(name + '.jpg', f.getvalue())

def get_temp_name():
    """Return a temporary file name."""
    return "test_%d" % random.randint(1,10000000)