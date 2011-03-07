from django.db import models
from . import VideoCardPort

class VideoCardHasPort(models.Model):
    quantity = models.IntegerField()
    port = models.ForeignKey(VideoCardPort)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + str(self.port)
        
    def raw_text(self):
        return self.port.raw_text()
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card has port'
        ordering = ['port', 'quantity']
