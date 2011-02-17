from django.db import models
from . import ProcessorL3CacheQuantity

class ProcessorL3Cache(models.Model):
    quantity = models.ForeignKey(ProcessorL3CacheQuantity)
    multiplier = models.IntegerField()
    
    def __unicode__(self):
        if self.multiplier == 0:
            return 'No posee'
        result = unicode(self.quantity)
        if self.multiplier > 1:
            result = unicode(self.multiplier) + 'x ' + result
        return result
        
    def is_valid(self):
        return self.multiplier
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['quantity', 'multiplier']
        app_label = 'cotizador'
