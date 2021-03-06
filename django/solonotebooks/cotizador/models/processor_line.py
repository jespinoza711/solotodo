from django.db import models
from . import ProcessorFamily

class ProcessorLine(models.Model):
    family = models.ForeignKey(ProcessorFamily)
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return unicode(self.family.brand) + ' ' + self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['family', 'name']
        app_label = 'cotizador'
