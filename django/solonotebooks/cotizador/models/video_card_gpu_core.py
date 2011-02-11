from django.db import models
from solonotebooks.cotizador.models import VideoCardGpuCoreFamily

class VideoCardGpuCore(models.Model):
    name = models.CharField(max_length = 255)
    family = models.ForeignKey(VideoCardGpuCoreFamily)
    
    def __unicode__(self):
        return unicode(self.family.architecture) + self.name
        
    def raw_text(self):
        return self.family.raw_text() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card GPU core family'
        ordering = ['family', 'name']
