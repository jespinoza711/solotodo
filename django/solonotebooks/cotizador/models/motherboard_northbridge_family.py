from django.db import models
from . import MotherboardChipsetBrand, MotherboardSocket

class MotherboardNorthbridgeFamily(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(MotherboardChipsetBrand)
    socket = models.ForeignKey(MotherboardSocket)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['brand']
