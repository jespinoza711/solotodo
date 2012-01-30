from django.db import models
from . import ProcessorFamily

class PowerSupplyPower(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return '%d W' % self.value
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
