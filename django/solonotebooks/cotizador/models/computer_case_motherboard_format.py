from django.db import models
from solonotebooks.cotizador.models.interface_motherboard_format import InterfaceMotherboardFormat

class ComputerCaseMotherboardFormat(models.Model):
    format = models.ForeignKey(InterfaceMotherboardFormat)
    
    def __unicode__(self):
        return unicode(self.format)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
