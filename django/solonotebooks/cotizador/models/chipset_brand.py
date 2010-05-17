from django.db import models

class ChipsetBrand(models.Model):
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
        
    def rawText(self):
        return self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Chipset brand'
        ordering = ['name']
