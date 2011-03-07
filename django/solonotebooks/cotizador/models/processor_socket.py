from django.db import models
from . import InterfaceSocket

class ProcessorSocket(models.Model):
    num_pins = models.IntegerField()
    name = models.CharField(max_length = 255)
    socket = models.ForeignKey(InterfaceSocket)
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['name']
        app_label = 'cotizador'
