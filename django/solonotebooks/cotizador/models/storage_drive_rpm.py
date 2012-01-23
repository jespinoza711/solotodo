from django.db import models

class StorageDriveRpm(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        if self.value > 0:
            return '%d rpm' % self.value
        else:
            return 'N/A'
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
