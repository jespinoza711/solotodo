from django.db import models

class StorageDriveBuffer(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        if self.value > 0:
            return '%d MB' % self.value
        else:
            return 'N/A'

    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['value']
