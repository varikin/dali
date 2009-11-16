import logging
import os
import re
import tempfile
import zipfile

from django import forms
from django.template.defaultfilters import slugify
from django.core.files import File

from gallery.models import Gallery, Picture

class ZipFileForm(forms.Form):
    gallery = forms.ModelChoiceField(queryset=Gallery.objects.all())
    zip_file = forms.FileField()

    valid_content_types = ('application/zip', 'application/x-zip',
            'application/x-zip-compressed', 'application/x-compress',
            'application/x-compressed', 'multipart/x-zip')
    valid_file_extensions = ('zip',)

    def clean_zip_file(self):
        """
        Returns the zip file as an UploadedFile if valid, else raises
        a ValidationError.
        """
        zf = self.cleaned_data['zip_file']
        if _file_ext(zf.name) in ZipFileForm.valid_file_extensions \
                and zf.content_type in ZipFileForm.valid_content_types:
            return zf
        raise forms.ValidationError("A zip file is required:)")

    def save(self):
        """
        Add all images in zip_file to gallery.

        Returns a list of names of invalid files in the zip file.
        """
        try:
            zip = zipfile.ZipFile(self.cleaned_data['zip_file'])
        except zipfile.BadZipfile:
            raise forms.ValidationError("The zip file is corrupted:(")

        files = {'valid': [], 'invalid': []}
        filenames = zip.namelist()
        for filename in filenames:
            name = _normalize_name(filename)
            slug = _unique_slug(name)
            pic = Picture(name=name, slug=slug, gallery=self.cleaned_data['gallery'])
            tf = tempfile.NamedTemporaryFile('wb+')
            tf.write(zip.read(filename))
            try:
                pic.original.save(filename, File(tf))
                files['valid'].append(filename)
            except IOError:
                files['invalid'].append(filename)
            tf.close()

        zip.close()
        return files

def _file_ext(filename):
    """Returns the extension of the filename as a lower case string."""
    return os.path.splitext(filename)[1][1:].lower()

def _normalize_name(name):
    """ 
    Returns a normalized name for the image.
    
    Removes the extension from the end.
    Removes leading paths.
    Replace underscores "_" with spaces " ".
    """
    
    logging.debug("name is [%s]", name)
    
    # Remove leading paths
    name = os.path.split(name)[1]
    
    # Remove all extentions
    # Seem to get many .jpg.jgp from Photoshop exports
    try:
        period = name.index('.')
        if period > 0:
            name = name[:period]
        else:
            name = name[1:]
    except ValueError:
        pass # Do nothing:)
    
    name = name.replace('_', ' ')
    
    logging.debug("resulting name is [%s]", name)
    return name

def _unique_slug(slug):
    """Returns a slug that is not in use."""
    slug = slugify(slug)
    count = 1
    name = slug
    while True:
        try:
            Picture.objects.get(slug=name)
        except Picture.DoesNotExist:
            return name
        else:
            name = "%s-%d" % (slug, count)
            count += 1
