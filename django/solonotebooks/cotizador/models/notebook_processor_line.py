from django.db import models
from . import NotebookProcessorLineFamily

class NotebookProcessorLine(models.Model):
    name = models.CharField(max_length = 255)
    family = models.ForeignKey(NotebookProcessorLineFamily)
    
    def __unicode__(self):
        return self.family.brand.name + ' ' + self.name
        
    def rawText(self):
        return self.family.rawText() + ' ' + self.name
        
    def tablePrint(self):
        return self.name        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor line'
        ordering = ['family', 'name']
