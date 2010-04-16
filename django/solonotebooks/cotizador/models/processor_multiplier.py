from django.db import models

class ProcessorMultiplier(models.Model):
    value = models.DecimalField(max_digits = 3, decimal_places = 1)
    
    def __unicode__(self):
        return unicode(self.value)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor multiplier'
        ordering = ['value']
