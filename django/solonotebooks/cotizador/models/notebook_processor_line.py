from django.db import models
from . import NotebookProcessorLineFamily

class NotebookProcessorLine(models.Model):
    name = models.CharField(max_length = 255)
    family = models.ForeignKey(NotebookProcessorLineFamily)
    
    def __unicode__(self):
        return unicode(self.family.brand) + ' ' + self.name
        
    def raw_text(self):
        return self.family.raw_text() + ' ' + self.name
        
    def tablePrint(self):
        return self.name        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor line'
        ordering = ['family', 'name']
