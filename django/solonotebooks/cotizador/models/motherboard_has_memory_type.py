from django.db import models
from . import MotherboardMemoryType

class MotherboardHasMemoryType(models.Model):
    quantity = models.IntegerField()
    mtype = models.ForeignKey(MotherboardMemoryType)
    
    def __unicode__(self):
        return str(self.quantity) + 'x ' + unicode(self.mtype)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['mtype']
