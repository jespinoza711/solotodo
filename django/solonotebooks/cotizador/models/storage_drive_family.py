from django.db import models
from solonotebooks.cotizador.models.storage_drive_brand import StorageDriveBrand

class StorageDriveFamily(models.Model):
    brand = models.ForeignKey(StorageDriveBrand)
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return '%s %s' % (unicode(self.brand), self.name)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['brand', 'name']
