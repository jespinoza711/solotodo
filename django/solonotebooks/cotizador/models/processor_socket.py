from django.db import models

class ProcessorSocket(models.Model):
    num_pins = models.IntegerField()
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = 'cotizador'
