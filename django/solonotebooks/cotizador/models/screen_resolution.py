from django.db import models
from . import ScreenAspectRatio

class ScreenResolution(models.Model):
    h_value = models.IntegerField()
    v_value = models.IntegerField()
    total_pixels = models.IntegerField()
    aspect_ratio = models.ForeignKey(ScreenAspectRatio)
    commercial_name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        value = str(self.h_value) + 'x' + str(self.v_value)
        if self.commercial_name.strip():
            value = self.commercial_name + ' (' + value + ')'
        return value
            
    class Meta:
        ordering = ['total_pixels']
        app_label = 'cotizador'
