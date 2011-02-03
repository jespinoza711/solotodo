from django.db import models
from . import NotebookProcessorLine, NotebookProcessorFrequency, NotebookProcessorSocket
from . import NotebookProcessorMultiplier, NotebookProcessorCache, NotebookProcessorFSB
from . import NotebookProcessorFamily

class NotebookProcessor(models.Model):
    name = models.CharField(max_length = 255)
    min_voltage = models.IntegerField()
    max_voltage = models.IntegerField()
    core_number = models.IntegerField()    
    tdp = models.DecimalField(max_digits = 4, decimal_places = 1)
    has_smp = models.BooleanField()
    has_turbo_mode = models.BooleanField()
    line = models.ForeignKey(NotebookProcessorLine)
    frequency = models.ForeignKey(NotebookProcessorFrequency)
    fsb = models.ForeignKey(NotebookProcessorFSB)
    multiplier = models.ForeignKey(NotebookProcessorMultiplier)
    cache = models.ForeignKey(NotebookProcessorCache)
    socket = models.ForeignKey(NotebookProcessorSocket)
    family = models.ForeignKey(NotebookProcessorFamily)
    speed_score = models.IntegerField()
    consumption = models.IntegerField()
    
    
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
        
    def pretty_print(self):
        return unicode(self.line) + ' ' + self.name + ' (' + unicode(self.frequency) + ')'
        
    def tablePrint(self):
        return self.line.tablePrint() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor'
        ordering = ('line', 'name')
