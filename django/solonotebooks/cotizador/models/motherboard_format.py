from django.db import models
from solonotebooks.cotizador.models.interface_motherboard_format import InterfaceMotherboardFormat

class MotherboardFormat(models.Model):
    format = models.ForeignKey(InterfaceMotherboardFormat, null=True)
    
    def __unicode__(self):
        return unicode(self.format)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
