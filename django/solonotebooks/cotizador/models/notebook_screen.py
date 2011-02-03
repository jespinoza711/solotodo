from django.db import models
from . import NotebookScreenResolution, NotebookScreenSize

class NotebookScreen(models.Model):
    is_glossy = models.BooleanField()
    is_touchscreen = models.BooleanField()
    is_led = models.BooleanField()
    is_rotating = models.BooleanField()
    resolution = models.ForeignKey(NotebookScreenResolution)
    size = models.ForeignKey(NotebookScreenSize)
    
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
        
    def rawText(self):
        resultado = self.size.rawText() + ' ' + self.resolution.rawText()
        if self.is_glossy:
            resultado += ' Opaca'
        else:
            resultado += ' Brillante Glossy'
        if self.is_led:
            resultado += ' LED'
        if self.is_touchscreen:
            resultado += ' Tactil Touchscreen'
        if self.is_rotating:
            resultado += ' Rotatoria'
        return resultado
        
    def pretty_display(self):
        return unicode(self.size) + ' (' + unicode(self.resolution) + ')'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook screen'
        ordering = ['size', 'resolution']
