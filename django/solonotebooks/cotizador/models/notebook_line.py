from django.db import models
from . import NotebookBrand

class NotebookLine(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(NotebookBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return self.brand.raw_text() + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook line'
        ordering = ['brand', 'name']
