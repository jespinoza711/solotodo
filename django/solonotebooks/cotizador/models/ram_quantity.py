from django.db import models

class RamQuantity(models.Model):
    value = models.DecimalField(max_digits = 3, decimal_places = 1)
    
    def __unicode__(self):
        return unicode(self.value) + ' GB'
        
    def rawText(self):
        return unicode(self.value) + ' GB'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'RAM Quantity'
        verbose_name_plural = 'RAM Quantities'
        ordering = ['value']
