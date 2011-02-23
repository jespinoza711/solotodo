from django.db import models

class ScreenDigitalTuner(models.Model):
    ordering = models.IntegerField()
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
            
    class Meta:
        ordering = ['ordering']
        app_label = 'cotizador'
