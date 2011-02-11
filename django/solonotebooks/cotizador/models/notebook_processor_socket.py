from django.db import models

class NotebookProcessorSocket(models.Model):
    name = models.CharField(max_length = 255)
    pincount = models.IntegerField()
    
    def __unicode__(self):
        return self.name + ' (' + unicode(self.pincount) + ')'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook processor socket'
        ordering = ['name']
