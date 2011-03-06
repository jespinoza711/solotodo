from django.db import models
from solonotebooks.cotizador.models import VideoCardPort, InterfaceVideoPort

class VideoCardHasPort(models.Model):
    old_port = models.ForeignKey(VideoCardPort)
    #port = models.ForeignKey(InterfaceVideoPort)
    quantity = models.IntegerField()
    
    port = property (lambda self: self.old_port)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + str(self.port)
        
    def raw_text(self):
        return self.port.raw_text()
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card has port'
        ordering = ['old_port', 'quantity']
