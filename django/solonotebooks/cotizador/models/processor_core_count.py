from django.db import models

class ProcessorCoreCount(models.Model):
    value = models.IntegerField()
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
