from django.db import models
from . import MotherboardVideoPort

class MotherboardHasVideoPort(models.Model):
    quantity = models.IntegerField()
    port = models.ForeignKey(MotherboardVideoPort)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + unicode(self.port)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['port', 'quantity']
