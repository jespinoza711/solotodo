from django.db import models

class VideoPort(models.Model):
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
        
    def rawText(self):
        return self.name        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video port'
        ordering = ['name']
