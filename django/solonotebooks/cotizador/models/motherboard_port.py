from django.db import models
from . import InterfacePort

class MotherboardPort(models.Model):
    port = models.ForeignKey(InterfacePort)
    
    def __unicode__(self):
        return unicode(self.port)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['port']
