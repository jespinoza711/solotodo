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
        
    def raw_text(self):
        result = str(self.h_value) + ' ' + str(self.v_value)
        result += ' ' + str(self.h_value) + 'x' + str(self.v_value)
        result += ' ' + self.commercial_name
        result += ' ' + self.aspect_ratio.raw_text()
        return result
            
    class Meta:
        ordering = ['-commercial_name', 'total_pixels']
        app_label = 'cotizador'
