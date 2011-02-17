from django.db import models

class ProcessorL3CacheQuantity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' MB'
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
