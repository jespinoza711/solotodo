from django.db import models

class VideoCardMemory(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' MB'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card memory'
        verbose_name_plural = 'Video card memory'
