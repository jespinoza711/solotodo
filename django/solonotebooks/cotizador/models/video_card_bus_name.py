from django.db import models

class VideoCardBusName(models.Model):
    name = models.CharField(max_length = 255)
    show_version_and_lanes = models.BooleanField()
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return self.name        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card bus name'
        ordering = ['name']
