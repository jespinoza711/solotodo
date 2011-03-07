from django.db import models
from . import MotherboardNorthbridgeFamily, MotherboardGraphics

class MotherboardNorthbridge(models.Model):
    name = models.CharField(max_length = 255)
    family = models.ForeignKey(MotherboardNorthbridgeFamily)
    graphics = models.ForeignKey(MotherboardGraphics)
    
    def __unicode__(self):
        return unicode(self.family.brand) + ' ' + self.name
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['family']
