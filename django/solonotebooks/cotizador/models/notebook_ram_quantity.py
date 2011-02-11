from django.db import models

class NotebookRamQuantity(models.Model):
    value = models.DecimalField(max_digits = 3, decimal_places = 1)
    
    def __unicode__(self):
        return unicode(self.value) + ' GB'
        
    def raw_text(self):
        return unicode(self.value) + ' GB'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Notebook RAM Quantity'
        verbose_name_plural = 'Notebook RAM Quantities'
        ordering = ['value']
