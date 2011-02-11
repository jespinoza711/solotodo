from django.db import models

class NotebookStorageDriveRpm(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' rpm'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook storage drive RPM'
        verbose_name_plural = 'Notebook storage drive RPM'
        ordering = ['value']
