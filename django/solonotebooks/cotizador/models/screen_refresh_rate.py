from django.db import models

class ScreenRefreshRate(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return str(self.value) + ' Hz'
        
    def raw_text(self):
        return unicode(self)
            
    class Meta:
        ordering = ['value']
        app_label = 'cotizador'
