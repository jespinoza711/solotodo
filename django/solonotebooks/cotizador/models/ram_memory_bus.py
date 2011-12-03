from django.db import models
from solonotebooks.cotizador.models.interface_memory_bus import InterfaceMemoryBus

class RamMemoryBus(models.Model):
    bus = models.ForeignKey(InterfaceMemoryBus)
    
    def __unicode__(self):
        return unicode(self.bus)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['bus']
        app_label = 'cotizador'
