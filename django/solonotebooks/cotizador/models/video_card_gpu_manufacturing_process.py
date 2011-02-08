from django.db import models

class VideoCardGpuManufacturingProcess(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.value) + ' nm'
       
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card GPU manufacturing process'
        ordering = ['value']
