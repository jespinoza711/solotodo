from django.db import models

class VideoCardMemoryQuantity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        if self.value % 1024:
            return str(self.value) + ' MB'
        else:
            return str(self.value / 1024) + ' GB'
       
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Video card memory quantity'
        ordering = ['value']
