from django.db import models

class RamFrequency(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' MHz'
        
    def rawText(self):
        return unicode(self.value) + ' MHz'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'RAM Frequency'
        verbose_name_plural = 'RAM Frequencies'
        ordering = ('value',)
