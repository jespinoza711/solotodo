from django.db import models
from . import ProcessorL1CacheQuantity

class ProcessorL1Cache(models.Model):
    quantity = models.ForeignKey(ProcessorL1CacheQuantity)
    multiplier = models.IntegerField()
    
    def __unicode__(self):
        if self.multiplier == 0:
            return 'No posee'
        result = unicode(self.quantity)
        if self.multiplier > 1:
            result = unicode(self.multiplier) + 'x ' + result
        return result
    
    class Meta:
        app_label = 'cotizador'
