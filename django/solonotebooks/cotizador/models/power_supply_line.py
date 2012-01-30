from django.db import models
from . import PowerSupplyBrand

class PowerSupplyLine(models.Model):
    brand = models.ForeignKey(PowerSupplyBrand)
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['brand', 'name']
        app_label = 'cotizador'
