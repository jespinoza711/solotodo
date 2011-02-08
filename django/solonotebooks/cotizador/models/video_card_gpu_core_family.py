from django.db import models
from solonotebooks.cotizador.models import VideoCardGpuArchitecture

class VideoCardGpuCoreFamily(models.Model):
    name = models.CharField(max_length = 255)
    architecture = models.ForeignKey(VideoCardGpuArchitecture)
    
    def __unicode__(self):
        return unicode(architecture) + self.name
        
    def raw_text(self):
        return architecture.raw_text() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card GPU core family'
        ordering = ['architecture', 'name']
