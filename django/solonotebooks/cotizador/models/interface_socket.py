from django.db import models
from . import InterfaceSocketBrand

class InterfaceSocket(models.Model):
    num_pins = models.IntegerField()
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(InterfaceSocketBrand)
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['brand', 'name']
        app_label = 'cotizador'
