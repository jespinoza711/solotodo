from django.db import models

class VideoCardGpuDirectxVersion(models.Model):
    value = models.DecimalField(max_digits = 3, decimal_places = 1)
    
    def __unicode__(self):
        return str(self.value)
        
    def raw_text(self):
        return str(self.value)  
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card GPU DirectX version'
        ordering = ['value']
