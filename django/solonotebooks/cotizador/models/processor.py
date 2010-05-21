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
    speed_score = models.IntegerField()
    
    
    def __unicode__(self):
        return unicode(self.line) + ' ' + self.name
        
    def rawText(self):
        result = self.name
        result += ' ' + self.line.rawText()
        result += ' ' + self.frequency.rawText()
        result += ' ' + self.family.rawText()
        if self.core_number == 1:
            result += ' single un core nucleo'
        elif self.core_number == 2:
            result += ' dual dos cores nucleos'
        elif self.core_number == 3:
            result += 'tri tres cores nucleos'
        elif self.core_number == 4:
            result += ' quad cuatro cores nucleos'
        
        return result
        
    def prettyPrint(self):
        return unicode(self.line) + ' ' + self.name + ' (' + unicode(self.frequency) + ')'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor'
        ordering = ('line', 'name')
