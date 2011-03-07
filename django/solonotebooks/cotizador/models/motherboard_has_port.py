from django.db import models
from . import MotherboardPort

class MotherboardHasPort(models.Model):
    quantity = models.IntegerField()
    port = models.ForeignKey(MotherboardPort)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + unicode(self.port)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['port', 'quantity']
