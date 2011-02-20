from django.db import models
from . import ScreenSizeFamily

class ScreenSize(models.Model):
    value = models.DecimalField(max_digits = 4, decimal_places = 1)
    family = models.ForeignKey(ScreenSizeFamily)
    
    def __unicode__(self):
        return str(self.value) + '"'
            
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
