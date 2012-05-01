from django.db import models
from . import InterfaceBrand
from solonotebooks.cotizador.models.computer_case_fan import ComputerCaseFan

class ComputerCaseFanDistribution(models.Model):
    quantity = models.IntegerField()
    fan = models.ForeignKey(ComputerCaseFan)
    
    def __unicode__(self):
        return '{0} x {1}'.format(self.quantity, self.fan)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['fan', 'quantity']
