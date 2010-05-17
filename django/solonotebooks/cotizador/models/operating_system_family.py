from django.db import models
from solonotebooks.cotizador.models import OperatingSystemBrand

class OperatingSystemFamily(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(OperatingSystemBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name

    def rawText(self):
        return self.brand.rawText() + ' ' + self.name    
        
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Operating system family'
        verbose_name_plural = 'Operating system families'
        ordering = ['brand', 'name']
