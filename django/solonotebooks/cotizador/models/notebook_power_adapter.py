from django.db import models

class NotebookPowerAdapter(models.Model):
    power = models.IntegerField()
    
    def __unicode__(self):
        if self.power > 0:
            return unicode(self.power) + ' W'
        else:
            return 'Desconocido'
            
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook Power adapter'
        ordering = ['power']
