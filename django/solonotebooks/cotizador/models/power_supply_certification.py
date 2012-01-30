from django.db import models

class PowerSupplyCertification(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
