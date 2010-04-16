from django.db import models
from solonotebooks.cotizador.models import NotebookBrand

class NotebookLine(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(NotebookBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook line'
        ordering = ['brand', 'name']
