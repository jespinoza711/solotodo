from django.db import models

class CellphoneRam(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.value) + ' MB'
        
    def raw_text(self):
        return str(self) + ' RAM'
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
