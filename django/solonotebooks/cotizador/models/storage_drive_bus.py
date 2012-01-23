from django.db import models
from solonotebooks.cotizador.models.interface_bus import InterfaceBus

class StorageDriveBus(models.Model):
    bus = models.ForeignKey(InterfaceBus)
    
    def __unicode__(self):
        return unicode(self.bus)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['bus']
