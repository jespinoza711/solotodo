from django.db import models
from . import ProcessorL2CacheQuantity

class ProcessorL2Cache(models.Model):
    quantity = models.ForeignKey(ProcessorL2CacheQuantity)
    multiplier = models.IntegerField()
    
    def __unicode__(self):
        if self.multiplier == 0:
            return 'No posee'
        result = unicode(self.quantity)
        if self.multiplier > 1:
            result = unicode(self.multiplier) + 'x ' + result
        return result
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['quantity', 'multiplier']
        app_label = 'cotizador'
