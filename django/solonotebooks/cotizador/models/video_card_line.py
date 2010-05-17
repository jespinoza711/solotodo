from django.db import models
from solonotebooks.cotizador.models import VideoCardBrand

class VideoCardLine(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(VideoCardBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def rawText(self):
        return self.brand.rawText() + ' ' + self.name        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card line'
        ordering = ['brand', 'name']
