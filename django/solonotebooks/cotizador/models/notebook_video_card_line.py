from django.db import models
from . import NotebookVideoCardBrand

class NotebookVideoCardLine(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(NotebookVideoCardBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def rawText(self):
        return self.brand.rawText() + ' ' + self.name        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook video card line'
        ordering = ['brand', 'name']
