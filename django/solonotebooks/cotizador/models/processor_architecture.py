from django.db import models
from . import ProcessorBrand

class ProcessorArchitecture(models.Model):
    brand = models.ForeignKey(ProcessorBrand)
    name = models.CharField(max_length = 255)
    turbo_step = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['brand']
        app_label = 'cotizador'
