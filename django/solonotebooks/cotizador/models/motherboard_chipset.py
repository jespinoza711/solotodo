from django.db import models
from . import MotherboardNorthbridge, MotherboardSouthbridge

class MotherboardChipset(models.Model):
    northbridge = models.ForeignKey(MotherboardNorthbridge)
    southbridge = models.ForeignKey(MotherboardSouthbridge)
    
    def __unicode__(self):
        return unicode(self.northbridge)
        
    def raw_text(self):
        return self.northbridge.raw_text() + ' ' + self.southbridge.raw_text()
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['northbridge']
