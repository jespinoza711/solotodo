from django.db import models

class ProcessorMultiplier(models.Model):
    value = models.DecimalField(max_digits = 3, decimal_places = 1)
    
    def __unicode__(self):
        return str(self.value) + 'x'
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
