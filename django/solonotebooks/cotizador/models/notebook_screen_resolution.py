from django.db import models

class NotebookScreenResolution(models.Model):
    horizontal = models.IntegerField()
    vertical = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.horizontal) + ' x ' + unicode(self.vertical)
        
    def raw_text(self):
        return unicode(self.horizontal) + ' ' + unicode(self.vertical)
        
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook screen resolution'
        ordering = ('horizontal', 'vertical',)
