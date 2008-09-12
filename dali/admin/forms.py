import re
from django import forms
from dali.models import Gallery

class ZipFileForm(forms.Form):
    gallery = forms.ModelChoiceField(queryset=Gallery.objects.all())
    zip_file = forms.FileField()
    

    def clean_zip_file(self):
        """
        Returns the zip file as an UploadedFile if valid, else raises
        a ValidationError.
        """
        zf = self.cleaned_data['zip_file']
        
        #There seems to be several valid mime types for a zip file such as:
        #application/zip, applicaiton/x-zip, application/x-compressed,
        #application/x-zip-compressed.  Validating based on whether mime type
        #contains zip or compressed.  
        if re.search("zip|compressed", zf.content_type):
            return zf
        else:
            raise forms.ValidationError("Invalid file, a zip file is required.")
            
    def save(self):
        """
        Add all images in zip_file to gallery.
        """
        pass
