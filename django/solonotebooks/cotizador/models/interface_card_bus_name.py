from django.db import models

class InterfaceCardBusName(models.Model):
    name = models.CharField(max_length = 255)
    show_version_and_lanes = models.BooleanField()
    
    def __unicode__(self):
        return self.name
        
    def raw_text(self):
        return self.name        
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['name']
