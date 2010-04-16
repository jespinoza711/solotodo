from django.db import models
from solonotebooks.cotizador.models import VideoCardType, VideoCardLine, VideoCardMemory

class VideoCard(models.Model):
    name = models.CharField(max_length = 255)
    gpu_frequency = models.IntegerField()
    memory_frequency = models.IntegerField()
    card_type = models.ForeignKey(VideoCardType)
    line = models.ForeignKey(VideoCardLine)
    memory = models.ForeignKey(VideoCardMemory)
    
    def __unicode__(self):
        return unicode(self.line) + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card'
        ordering = ['line', 'name']
