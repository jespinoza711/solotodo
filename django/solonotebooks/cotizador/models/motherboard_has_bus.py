from django.db import models
from . import MotherboardBus

class MotherboardHasBus(models.Model):
    quantity = models.IntegerField()
    bus = models.ForeignKey(MotherboardBus)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + unicode(self.bus)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['bus', 'quantity']
