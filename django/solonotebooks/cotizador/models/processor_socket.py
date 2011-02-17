from django.db import models

class ProcessorSocket(models.Model):
    num_pins = models.IntegerField()
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['name']
        app_label = 'cotizador'
