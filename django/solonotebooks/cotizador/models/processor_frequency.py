from django.db import models

class ProcessorFrequency(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' MHz'
        
    def rawText(self):
        return unicode(self.value) + ' MHz'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor frequency'
        verbose_name_plural = 'Processor frequencies'
        ordering = ('value',)
