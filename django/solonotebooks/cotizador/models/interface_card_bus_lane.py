from django.db import models

class InterfaceCardBusLane(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return  'x' + str(self.value)
        
    def raw_text(self):
        return unicode(self)
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
