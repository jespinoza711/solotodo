from django.db import models

class ScreenRefreshRate(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.value) + ' MHz'
            
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
