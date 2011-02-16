from django.db import models

class ProcessorFsb(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.value) + ' MHz'
    
    class Meta:
        app_label = 'cotizador'
