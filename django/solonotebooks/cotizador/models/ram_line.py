from django.db import models
from solonotebooks.cotizador.models.ram_brand import RamBrand

class RamLine(models.Model):
    brand = models.ForeignKey(RamBrand)
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['brand', 'name']
        app_label = 'cotizador'
