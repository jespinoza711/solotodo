from django.db import models
from . import ScreenDisplayType

class ScreenDisplay(models.Model):
    backlight = models.CharField(max_length = 255)
    dtype = models.ForeignKey(ScreenDisplayType)
    
    def __unicode__(self):
        return unicode(self.dtype) + ' ' + self.backlight
            
    class Meta:
        ordering = ['dtype']
        app_label = 'cotizador'
