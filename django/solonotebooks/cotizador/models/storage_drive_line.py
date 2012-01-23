from django.db import models
from solonotebooks.cotizador.models.storage_drive_family import StorageDriveFamily

class StorageDriveLine(models.Model):
    family = models.ForeignKey(StorageDriveFamily)
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return '%s %s' % (unicode(self.family), self.name)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['family', 'name']
