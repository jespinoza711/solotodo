from django.db import models

class StorageDriveType(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return unicode(self.name)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['name']
