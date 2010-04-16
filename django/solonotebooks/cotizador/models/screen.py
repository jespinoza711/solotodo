from django.db import models
from solonotebooks.cotizador.models import ScreenResolution, ScreenSize

class Screen(models.Model):
    is_glossy = models.BooleanField()
    is_touchscreen = models.BooleanField()
    is_led = models.BooleanField()
    is_rotating = models.BooleanField()
    resolution = models.ForeignKey(ScreenResolution)
    size = models.ForeignKey(ScreenSize)
    
    def __unicode__(self):
        resultado =  unicode(self.size) + ' (' + unicode(self.resolution) + ')'
        if (not self.is_glossy):
            resultado += ' [Opaca]'
        if (self.is_led):
            resultado += ' [LED]'
        if (self.is_touchscreen):
            resultado += ' [Tactil]'
        if (self.is_rotating):
            resultado += ' [Rotatoria]'
        return resultado
        
    def prettyDisplay(self):
        return unicode(self.size) + ' (' + unicode(self.resolution) + ')'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Screen'
        ordering = ['size', 'resolution']
