from django.db import models
from . import InterfaceVideoPort

class VideoCardPort(models.Model):
    port = models.ForeignKey(InterfaceVideoPort)
    
    def __unicode__(self):
        return unicode(self.port)
        
    def raw_text(self):
        return unicode(self.port)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['port']
