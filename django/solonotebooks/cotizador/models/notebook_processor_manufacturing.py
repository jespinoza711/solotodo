from django.db import models

class NotebookProcessorManufacturing(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' nm'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor manufaturing'
        ordering = ['value']
