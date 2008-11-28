from os.path import splitext
import re
import tempfile
import zipfile
from django import forms
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
            name = splitext(filename)[0]
            slug = _unique_webname(name)
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
    return splitext(filename)[1][1:].lower()

def _unique_webname(webname):
    """Returns a slug that is not in use."""
    webname = re.sub('\W', "_", webname)
    count = 1
    name = webname
    while True:
        try:
            Picture.objects.get(slug=name)
        except Picture.DoesNotExist:
            return name
        else:
            name = "%s_%d" % (webname, count)
            count += 1