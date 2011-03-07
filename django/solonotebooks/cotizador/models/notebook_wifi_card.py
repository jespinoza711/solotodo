from django.db import models
from . import NotebookWifiCardBrand, NotebookWifiCardNorm

class NotebookWifiCard(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(NotebookWifiCardBrand)
    norm = models.ForeignKey(NotebookWifiCardNorm)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name + ' (' + unicode(self.norm) + ')'
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook wifi card'
        ordering = ['brand', 'name', 'norm']
