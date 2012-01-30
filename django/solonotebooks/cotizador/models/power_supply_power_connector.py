from django.db import models
from . import InterfacePowerConnector

class PowerSupplyPowerConnector(models.Model):
    connector = models.ForeignKey(InterfacePowerConnector)
    
    def __unicode__(self):
        return unicode(self.connector)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['connector']
