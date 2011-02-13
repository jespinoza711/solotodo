from django.db import models
from solonotebooks.cotizador.models import VideoCardGpuBrand

class VideoCardGpuFamily(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(VideoCardGpuBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return self.brand.raw_text() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card GPU family'
        ordering = ['brand', 'name']
