from django.db import models
from . import NotebookProcessorManufacturing

class NotebookProcessorFamily(models.Model):
    name = models.CharField(max_length = 255)
    nm = models.ForeignKey(NotebookProcessorManufacturing)
    
    def __unicode__(self):
        return self.name + ' (' + unicode(self.nm) + ')'
        
    def raw_text(self):
        return self.name + ' ' + unicode(self.nm) + ' nm'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor family'
        verbose_name_plural = 'Notebook processor families'
        ordering = ['name',]
