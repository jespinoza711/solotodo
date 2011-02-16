from django.db import models
from . import ProcessorBrand

class ProcessorLine(models.Model):
    brand = models.ForeignKey(ProcessorBrand)
    name = models.CharField(max_length = 255)
    separator = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return unicode(self.brand) + self.name
    
    class Meta:
        app_label = 'cotizador'
