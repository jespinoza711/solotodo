from django.db import models

class NotebookProcessorCache(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + " KB"
    
    class Meta:
        verbose_name = 'Notebook processor cache'
        app_label = 'cotizador'
        ordering = ('value',)
