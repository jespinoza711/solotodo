from django.db import models
from . import InterfaceBrand

class ComputerCasePowerSupply(models.Model):
    power = models.IntegerField()
    
    def __unicode__(self):
        if self.power:
            return '{0} W.'.format(self.power)
        else:
            return 'No posee'
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['power']
