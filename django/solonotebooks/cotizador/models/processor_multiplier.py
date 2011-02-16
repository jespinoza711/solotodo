from django.db import models

class ProcessorMultiplier(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.value) + 'x'
    
    class Meta:
        app_label = 'cotizador'
