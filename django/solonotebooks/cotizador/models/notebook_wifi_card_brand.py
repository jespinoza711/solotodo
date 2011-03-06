from django.db import models
from . import InterfaceBrand

class NotebookWifiCardBrand(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(InterfaceBrand)
    
    def __unicode__(self):
        return unicode(self.brand)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook wifi card brand'
