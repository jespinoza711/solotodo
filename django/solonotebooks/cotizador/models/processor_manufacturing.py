from django.db import models

class ProcessorManufacturing(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' nm'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor manufaturing'
        ordering = ['value']
