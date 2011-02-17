from django.db import models

class ProcessorL2CacheQuantity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' KB'
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
