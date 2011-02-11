from django.db import models
from . import NotebookOperatingSystemBrand

class NotebookOperatingSystemFamily(models.Model):
    name = models.CharField(max_length = 255)
    brand = models.ForeignKey(NotebookOperatingSystemBrand)
    
    def __unicode__(self):
        return unicode(self.brand) + ' ' + self.name

    def raw_text(self):
        return self.brand.raw_text() + ' ' + self.name    
        
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook Operating system family'
        verbose_name_plural = 'Notebook Operating system families'
        ordering = ['brand', 'name']
