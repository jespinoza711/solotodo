from django.db import models
from solonotebooks.cotizador.models import VideoCardPort

class VideoCardHasPort(models.Model):
    port = models.ForeignKey(VideoCardPort)
    quantity = models.IntegerField()
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + self.name
        
    def raw_text(self):
        return self.port.raw_text()
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card has port'
        ordering = ['port', 'quantity']
