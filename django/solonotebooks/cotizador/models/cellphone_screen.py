#-*- coding: UTF-8 -*-
from django.db import models
from . import CellphoneScreenSize, CellphoneScreenResolution, CellphoneScreenColors

class CellphoneScreen(models.Model):
    size = models.ForeignKey(CellphoneScreenSize)
    resolution = models.ForeignKey(CellphoneScreenResolution)
    colors = models.ForeignKey(CellphoneScreenColors)
    is_touch = models.BooleanField()
    
    def __unicode__(self):
        result = str(self.size)
        if self.is_touch:
            result += u' tactil'
        result += ' (' + str(self.resolution) + ')'
        return result
        
    def raw_text(self):
        return str(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['size', 'resolution']
