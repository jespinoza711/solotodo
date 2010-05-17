from django.db import models
from solonotebooks.cotizador.models import ChipsetBrand

class Chipset(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(ChipsetBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def rawText(self):
        return self.brand.rawText() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Chipset'
        ordering = ['brand', 'name']
