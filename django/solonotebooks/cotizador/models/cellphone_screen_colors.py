from django.db import models

class CellphoneScreenColors(models.Model):
    quantity = models.IntegerField()
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return str(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['quantity']
