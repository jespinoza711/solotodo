from django.db import models
from . import InterfaceBrand

class NotebookOperatingSystemBrand(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(InterfaceBrand)
    
    def __unicode__(self):
        return unicode(self.brand)
        
    def raw_text(self):
        return self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook Operating system brand'
