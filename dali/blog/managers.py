from django.db import models

class PostManager(models.Manager):
    """Custom manager for the Post model."""
    
    def published(self):
        """Returns only the published posts."""
        return self.filter(published=True)
