from django.db import models
from . import MotherboardNorthbridge, MotherboardSouthbridge

class MotherboardChipset(models.Model):
    name = models.CharField(max_length = 255)
    northbridge = models.ForeignKey(MotherboardNorthbridge)
    southbridge = models.ForeignKey(MotherboardSouthbridge)
    
    def pretty_display(self):
        return unicode(self.northbridge.family.brand) + ' ' + self.name
        
    def __unicode__(self):
        return '%s (%s)' % (self.pretty_display(), unicode(self.northbridge.family.socket))
        
    def raw_text(self):
        return self.name + ' ' + self.northbridge.raw_text() + ' ' + self.southbridge.raw_text()
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['northbridge']
