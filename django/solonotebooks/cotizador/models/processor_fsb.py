from django.db import models

class ProcessorFSB(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + " MHz"
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor FSB'
        verbose_name_plural = 'Processor FSB'
        ordering = ('value',)
