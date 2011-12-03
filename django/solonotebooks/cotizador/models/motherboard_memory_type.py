from django.db import models
from . import InterfaceMemoryType
from solonotebooks.cotizador.models.interface_memory_bus import InterfaceMemoryBus

class MotherboardMemoryType(models.Model):
    itype = models.ForeignKey(InterfaceMemoryBus, blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.itype)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['itype']
