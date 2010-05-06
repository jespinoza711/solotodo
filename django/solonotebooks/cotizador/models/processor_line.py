from django.db import models
from solonotebooks.cotizador.models import ProcessorLineFamily

class ProcessorLine(models.Model):
    name = models.CharField(max_length = 255)
    family = models.ForeignKey(ProcessorLineFamily)
    
    def __unicode__(self):
        return self.family.brand.name + ' ' + self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Processor line'
        ordering = ['family', 'name']
