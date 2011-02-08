from django.db import models

class NotebookRamType(models.Model):
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name

    def raw_text(self):
        return self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook RAM Type'
        ordering = ['name']
