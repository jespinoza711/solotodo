from django.db import models
from solonotebooks.cotizador.models import ProcessorManufacturing

class ProcessorFamily(models.Model):
    name = models.CharField(max_length = 255)
    nm = models.ForeignKey(ProcessorManufacturing)
    
    def __unicode__(self):
        return self.name + ' (' + unicode(self.nm) + ')'
        
    def rawText(self):
        return self.name + ' ' + unicode(self.nm) + ' nm'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor family'
        verbose_name_plural = 'Processor families'
        ordering = ['name',]
