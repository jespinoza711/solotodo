from django.db import models

class NotebookProcessorFSB(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + " MHz"
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor FSB'
        verbose_name_plural = 'Notebook processor FSB'
        ordering = ('value',)
