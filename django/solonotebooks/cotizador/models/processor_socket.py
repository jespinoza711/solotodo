from django.db import models
from . import InterfaceSocket

class ProcessorSocket(models.Model):
    socket = models.ForeignKey(InterfaceSocket)
    
    def __unicode__(self):
        return str(self.socket)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['socket']
        app_label = 'cotizador'
