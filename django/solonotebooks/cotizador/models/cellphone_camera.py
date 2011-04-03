from django.db import models

class CellphoneCamera(models.Model):
    mp = models.DecimalField(max_digits = 3, decimal_places = 1)
    
    def __unicode__(self):
        if self.mp:
            return str(self.value) + ' MP'
        else:
            return 'No posee'
        
    def raw_text(self):
        return str(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['mp']
