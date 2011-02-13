from django.db import models

class VideoCardBusLane(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return  'x' + str(self.value)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card bus lane'
        ordering = ['value']
