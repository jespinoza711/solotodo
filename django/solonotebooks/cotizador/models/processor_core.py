from django.db import models
from . import ProcessorManufacturingProcess, ProcessorArchitecture

class ProcessorCore(models.Model):
    name = models.CharField(max_length = 255)
    architecture = models.ForeignKey(ProcessorArchitecture)
    manufacturing_processs = models.ForeignKey(ProcessorManufacturingProcess)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = 'cotizador'
