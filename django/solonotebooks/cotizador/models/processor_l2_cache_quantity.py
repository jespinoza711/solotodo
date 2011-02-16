from django.db import models

class ProcessorL2CacheQuantity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' MB'
    
    class Meta:
        app_label = 'cotizador'
