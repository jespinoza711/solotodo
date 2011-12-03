from django.db import models
from solonotebooks.cotizador.models.ram_frequency import RamFrequency
from solonotebooks.cotizador.models.ram_memory_bus import RamMemoryBus

class RamBus(models.Model):
    bus = models.ForeignKey(RamMemoryBus)
    frequency = models.ForeignKey(RamFrequency)
    
    def __unicode__(self):
        return u'%s (%s)' % (unicode(self.bus),  unicode(self.frequency))

    def title_display(self):
        return '%s %s-%s' % (unicode(self.bus.bus.format), unicode(self.bus.bus.type), unicode(self.frequency.value))
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['bus', 'frequency']
        app_label = 'cotizador'
