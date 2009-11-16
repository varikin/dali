from django.db import models

class GalleryManager(models.Manager):
    """Custom manager for the Gallery model."""
    
    def published(self):
        """Returns only the published galleries."""
        return self.filter(published=True)
