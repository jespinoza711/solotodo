from django.db import models
from . import NotebookVideoCardBrand

class NotebookVideoCardLine(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(NotebookVideoCardBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name
        
    def raw_text(self):
        return self.brand.raw_text() + ' ' + self.name        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook video card line'
        ordering = ['brand', 'name']
