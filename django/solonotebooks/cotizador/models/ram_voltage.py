from django.db import models

class RamVoltage(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=1)
    
    def __unicode__(self):
        return unicode(self.value) + ' V'
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
