from django.db import models

class PreferenceManager(models.Manager):
    """
    Custom manager for the Preference model.  Provides a method to get the only
    preference in the system.
    """
    
    def get_preference(self):
        """Returns the only preference in the system or None."""
        try:
            return super(PreferenceManager, self).all()[0]
        except IndexError:
            return None
