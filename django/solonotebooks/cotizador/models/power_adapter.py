from django.db import models

class PowerAdapter(models.Model):
    power = models.IntegerField()
    
    def __unicode__(self):
        if self.power > 0:
            return unicode(self.power) + ' W'
        else:
            return 'Desconocido'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Power adapter'
        ordering = ['power']
