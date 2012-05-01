from django.db import models
from . import InterfaceBrand

class ComputerCaseFan(models.Model):
    mm = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.mm) + ' mm.'
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['mm']
