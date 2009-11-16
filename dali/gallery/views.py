from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import list_detail
from gallery.models import Picture, Gallery

def privileged_gallery_queryset(view):
    """
    Decorator to set the gallery queryset.

    If the user is authenticated, return all galleries, else only the published ones.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            kwargs['queryset'] = Gallery.objects.all()
        else:
            kwargs['queryset'] = Gallery.objects.published()
        return view(request, *args, **kwargs)
    return _wrapped_view

@privileged_gallery_queryset
def gallery_detail(request, gallery=None, queryset=None):
    """View to show a specific gallery."""
    context = {}
    if gallery is not None:
        try:
            gallery  = queryset.get(slug=gallery)
            context['gallery'] = gallery
            context['pictures'] = Picture.objects.filter(gallery=gallery)
        except Gallery.DoesNotExist:
            raise Http404
    
    context['gallery_list'] = queryset.filter(parent_gallery=gallery)
    return render_to_response('gallery/gallery_detail.html', context)

def picture_detail(request, gallery, picture):
    """View to show a specific picture."""
    try:
        context = { 'picture': Picture.objects.get(slug=picture) }
    except Picture.DoesNotExist: 
        raise Http404
    return render_to_response('gallery/picture_detail.html', context)

def choose_gallery(request):
    """For the dali_advimage TinyMCE plugin"""
    context = { 'galleries': Gallery.objects.published() }
    return render_to_response('gallery/choose_gallery.html', context)

def choose_picture(request, gallery):
    """For the dali_advimage TinyMCE plugin"""
    context = { 'pictures': Picture.objects.filter(gallery__slug=gallery) }
    return render_to_response('gallery/choose_picture.html', context)
