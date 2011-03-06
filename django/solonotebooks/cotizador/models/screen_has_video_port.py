from django.db import models
from . import ScreenVideoPort, InterfaceVideoPort

class ScreenHasVideoPort(models.Model):
    quantity = models.IntegerField()
    old_port = models.ForeignKey(ScreenVideoPort)
    #port = models.ForeignKey(InterfaceVideoPort)
    
    port = property (lambda self: self.old_port)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + unicode(self.port)
        
    def raw_text(self):
        return self.port.raw_text()
            
    class Meta:
        ordering = ['old_port', 'quantity']
        app_label = 'cotizador'
