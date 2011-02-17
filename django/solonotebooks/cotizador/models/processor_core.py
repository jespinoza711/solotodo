from django.db import models
from . import ProcessorManufacturingProcess, ProcessorArchitecture

class ProcessorCore(models.Model):
    name = models.CharField(max_length = 255)
    architecture = models.ForeignKey(ProcessorArchitecture)
    manufacturing_process = models.ForeignKey(ProcessorManufacturingProcess)
    
    def __unicode__(self):
        return unicode(self.architecture.brand) + ' ' + self.name
        
    def raw_text(self):
        return self.architecture.raw_text() + ' ' + self.manufacturing_process.raw_text() + ' ' + unicode(self)
    
    class Meta:
        ordering = ['architecture', 'name']
        app_label = 'cotizador'
