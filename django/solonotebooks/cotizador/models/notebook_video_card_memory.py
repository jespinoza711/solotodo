from django.db import models

class NotebookVideoCardMemory(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' MB'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook video card memory'
        verbose_name_plural = 'Notebook video card memory'
