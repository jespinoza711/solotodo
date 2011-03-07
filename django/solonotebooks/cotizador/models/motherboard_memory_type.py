from django.db import models
from . import InterfaceMemoryType

class MotherboardMemoryType(models.Model):
    mtype = models.ForeignKey(InterfaceMemoryType)
    
    def __unicode__(self):
        return unicode(self.mtype)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['mtype']
