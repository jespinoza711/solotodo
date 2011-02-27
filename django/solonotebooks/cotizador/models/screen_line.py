from django.db import models
from . import ScreenBrand

class ScreenLine(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(ScreenBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return self.brand.raw_text() + ' ' + self.name
            
    class Meta:
        ordering = ['brand', 'name']
        app_label = 'cotizador'
