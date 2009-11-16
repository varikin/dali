from django import forms

class PostForm(forms.Form):
    """
    Form for a Post.
    
    This is currently only used for the ajax inplace update where only
    title, body, and published are updated. None of them are required,
    because this is not used to create a new Post (yet:)
    """
    title = forms.CharField(max_length=100, required=False)
    body = forms.CharField(required=False)
    published= forms.BooleanField(required=False)
