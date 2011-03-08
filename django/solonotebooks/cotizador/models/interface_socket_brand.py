from django.db import models
from . import InterfaceBrand

class InterfaceSocketBrand(models.Model):
    brand = models.ForeignKey(InterfaceBrand)
    
    def __unicode__(self):
        return unicode(self.brand)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['brand']
        app_label = 'cotizador'
