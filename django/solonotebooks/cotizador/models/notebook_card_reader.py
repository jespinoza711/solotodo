from django.db import models

class NotebookCardReader(models.Model):
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook card reader'
        ordering = ['name']
