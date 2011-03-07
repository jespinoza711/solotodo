from django.db import models
from . import MotherboardCardBus

class MotherboardHasCardBus(models.Model):
    quantity = models.IntegerField()
    bus = models.ForeignKey(MotherboardCardBus)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + unicode(self.bus)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['bus', 'quantity']
