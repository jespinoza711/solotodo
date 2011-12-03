from django.db import models

class RamVoltage(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=2)
    
    def __unicode__(self):
        return unicode(self.value) + ' V'
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
