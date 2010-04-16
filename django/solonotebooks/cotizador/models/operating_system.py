from django.db import models
from solonotebooks.cotizador.models import OperatingSystemFamily, OperatingSystemLanguage

class OperatingSystem(models.Model):
    name = models.CharField(max_length = 255)
    is_64_bit = models.BooleanField()
    family = models.ForeignKey(OperatingSystemFamily)
    language = models.ForeignKey(OperatingSystemLanguage)
    
    def __unicode__(self):
        result = unicode(self.family) + ' ' + self.name
        if self.is_64_bit:
            result += ' (64 bits)'
        return result
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Operating system'
        ordering = ['family', 'name']
