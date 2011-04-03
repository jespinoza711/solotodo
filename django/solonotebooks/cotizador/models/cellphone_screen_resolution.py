from django.db import models

class CellphoneScreenResolution(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    total_pixels = models.IntegerField()
    
    def __unicode__(self):
        return str(self.width) + 'x' + str(self.height)
        
    def raw_text(self):
        return str(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['total_pixels']
