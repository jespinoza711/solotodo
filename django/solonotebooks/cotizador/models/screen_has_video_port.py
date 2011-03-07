from django.db import models
from . import ScreenVideoPort

class ScreenHasVideoPort(models.Model):
    quantity = models.IntegerField()
    port = models.ForeignKey(ScreenVideoPort)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + unicode(self.port)
        
    def raw_text(self):
        return self.port.raw_text()
            
    class Meta:
        ordering = ['port', 'quantity']
        app_label = 'cotizador'
