from django.db import models
from . import InterfaceBrand

class CellphoneManufacturer(models.Model):
    brand = models.ForeignKey(InterfaceBrand)
    
    def __unicode__(self):
        return str(self.brand)
        
    def raw_text(self):
        return str(self.brand)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['brand']
