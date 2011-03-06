from django.db import models
from . import InterfaceBrand

class VideoCardGpuBrand(models.Model):
    brand = models.ForeignKey(InterfaceBrand)
    name = property(lambda self: self.brand.name)
    
    def __unicode__(self):
        return unicode(self.brand)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['brand']
