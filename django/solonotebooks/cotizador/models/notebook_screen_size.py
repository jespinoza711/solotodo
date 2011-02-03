from django.db import models
from . import NotebookScreenSizeFamily

class NotebookScreenSize(models.Model):
    size = models.DecimalField(max_digits = 3, decimal_places = 1)
    family = models.ForeignKey(NotebookScreenSizeFamily)
    
    def __unicode__(self):
        return unicode(self.size) + '"'
        
    def titleText(self):
        return unicode(self.size) + ' pulgadas'
        
    def rawText(self):
        return unicode(self.size) + ' ' + self.family.rawText()
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook screen size'
        ordering = ('size',)
