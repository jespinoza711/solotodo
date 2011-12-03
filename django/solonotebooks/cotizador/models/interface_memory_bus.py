from django.db import models
from solonotebooks.cotizador.models.interface_memory_format import InterfaceMemoryFormat
from solonotebooks.cotizador.models.interface_memory_type import InterfaceMemoryType

class InterfaceMemoryBus(models.Model):
    format = models.ForeignKey(InterfaceMemoryFormat)
    type = models.ForeignKey(InterfaceMemoryType)
    pincount = models.IntegerField()
    
    def __unicode__(self):
        return '%s %s' % (unicode(self.format), unicode(self.type), )
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['format', 'type']
