from django.db import models

class CellphoneScreenSize(models.Model):
    value = models.DecimalField(max_digits = 2, decimal_places = 1)
    
    def __unicode__(self):
        return str(self.value) + '"'
        
    def raw_text(self):
        return str(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
