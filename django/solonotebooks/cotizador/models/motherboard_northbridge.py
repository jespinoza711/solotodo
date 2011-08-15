from django.db import models
from . import MotherboardNorthbridgeFamily, MotherboardGraphics

class MotherboardNorthbridge(models.Model):
    name = models.CharField(max_length = 255)
    family = models.ForeignKey(MotherboardNorthbridgeFamily)
    graphics = models.ForeignKey(MotherboardGraphics)
    
    def __unicode__(self):
        return '%s %s (%s)' % (unicode(self.family.brand), self.name, unicode(self.family.socket))
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['family']
