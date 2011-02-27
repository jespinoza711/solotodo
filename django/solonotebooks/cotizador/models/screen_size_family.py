from django.db import models

class ScreenSizeFamily(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.value) + '"'
        
    def raw_text(self):
        return str(self.value)
            
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
