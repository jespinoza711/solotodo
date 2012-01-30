from django.db import models
from . import PowerSupplyPowerConnector

class PowerSupplyHasPowerConnector(models.Model):
    quantity = models.IntegerField()
    connector = models.ForeignKey(PowerSupplyPowerConnector)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + unicode(self.connector)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['connector', 'quantity']
