from django.db import models
from solonotebooks.cotizador.models import VideoCardGpuFamily

class VideoCardGpuLine(models.Model):
    name = models.CharField(max_length = 255)
    family = models.ForeignKey(VideoCardGpuFamily)
    
    def __unicode__(self):
        return unicode(family) + self.name
        
    def raw_text(self):
        return family.raw_text() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card GPU family'
        ordering = ['family', 'name']
