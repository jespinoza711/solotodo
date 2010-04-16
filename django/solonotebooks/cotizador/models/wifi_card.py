from django.db import models
from solonotebooks.cotizador.models import WifiCardBrand, WifiCardNorm

class WifiCard(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(WifiCardBrand)
    norm = models.ForeignKey(WifiCardNorm)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name + ' (' + unicode(self.norm) + ')'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Wifi card'
        ordering = ['brand', 'name', 'norm']
