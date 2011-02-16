from django.db import models

class ProcessorL1CacheQuantity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' KB'
    
    class Meta:
        app_label = 'cotizador'
