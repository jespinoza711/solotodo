from django.db import models

class NotebookStorageDriveCapacity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' GB'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook Storage drive capacity'
        verbose_name_plural = 'Notebook Storage drive capacities'
        ordering = ['value']
