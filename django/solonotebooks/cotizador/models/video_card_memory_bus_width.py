from django.db import models

class VideoCardMemoryBusWidth(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.value) + ' bit'
       
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card memory quantity'
        ordering = ['value']
