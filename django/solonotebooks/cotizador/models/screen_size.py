from django.db import models
from solonotebooks.cotizador.models import ScreenSizeFamily

class ScreenSize(models.Model):
    size = models.DecimalField(max_digits = 3, decimal_places = 1)
    family = models.ForeignKey(ScreenSizeFamily)
    
    def __unicode__(self):
        return unicode(self.size) + '"'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Screen size'
        ordering = ('size',)
