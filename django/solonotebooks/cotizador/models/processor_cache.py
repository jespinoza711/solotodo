from django.db import models

class ProcessorCache(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + " KB"
    
    class Meta:
        verbose_name = 'Processor cache'
        app_label = 'cotizador'
        ordering = ('value',)
