from django.db import models

class NotebookProcessorFrequency(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' MHz'
        
    def raw_text(self):
        return unicode(self.value) + ' MHz'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor frequency'
        verbose_name_plural = 'Notebook processor frequencies'
        ordering = ('value',)
