from django.db import models
from solonotebooks.cotizador.models import ProcessorLine, ProcessorFrequency, ProcessorSocket
from solonotebooks.cotizador.models import ProcessorMultiplier, ProcessorCache, ProcessorFSB
from solonotebooks.cotizador.models import ProcessorFamily

class Processor(models.Model):
    name = models.CharField(max_length = 255)
    min_voltage = models.IntegerField()
    max_voltage = models.IntegerField()
    core_number = models.IntegerField()    
    tdp = models.DecimalField(max_digits = 4, decimal_places = 1)
    has_smp = models.BooleanField()
    has_turbo_mode = models.BooleanField()
    line = models.ForeignKey(ProcessorLine)
    frequency = models.ForeignKey(ProcessorFrequency)
    fsb = models.ForeignKey(ProcessorFSB)
    multiplier = models.ForeignKey(ProcessorMultiplier)
    cache = models.ForeignKey(ProcessorCache)
    socket = models.ForeignKey(ProcessorSocket)
    family = models.ForeignKey(ProcessorFamily)
    
    
    def __unicode__(self):
        return unicode(self.line) + ' ' + self.name
        
    def prettyPrint(self):
        return unicode(self.line) + ' ' + self.name + ' (' + unicode(self.frequency) + ')'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor'
        ordering = ('line', 'name')
