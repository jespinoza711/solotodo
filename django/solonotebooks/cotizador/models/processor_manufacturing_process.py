from django.db import models

class ProcessorManufacturingProcess(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' nm'
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
