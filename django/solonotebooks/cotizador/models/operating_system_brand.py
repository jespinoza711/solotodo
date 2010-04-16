from django.db import models

class OperatingSystemBrand(models.Model):
    name = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Operating system brand'
