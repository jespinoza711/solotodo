from django.db import models

class RamTotalCapacity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        if self.value % 1024 == 0:
            return unicode(self.value / 1024) + ' GB'
        else:
            return unicode(self.value) + ' MB'
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
