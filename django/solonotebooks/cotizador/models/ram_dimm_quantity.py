from django.db import models

class RamDimmQuantity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
