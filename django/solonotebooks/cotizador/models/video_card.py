from django.db import models
from solonotebooks.cotizador.models import VideoCardType, VideoCardLine, VideoCardMemory

class VideoCard(models.Model):
    name = models.CharField(max_length = 255)
    gpu_frequency = models.IntegerField()
    memory_frequency = models.IntegerField()
    card_type = models.ForeignKey(VideoCardType)
    line = models.ForeignKey(VideoCardLine)
    memory = models.ForeignKey(VideoCardMemory)
    speed_score = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.line) + ' ' + self.name
        
    def rawText(self):
        return self.line.rawText() + ' ' + self.card_type.rawText() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card'
        ordering = ['line', 'name']
