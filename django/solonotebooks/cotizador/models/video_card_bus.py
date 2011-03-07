from django.db import models
from solonotebooks.cotizador.models import InterfaceCardBus

class VideoCardBus(models.Model):
    bus = models.ForeignKey(InterfaceCardBus)
    
    def __unicode__(self):
        return unicode(self.bus)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['bus']
