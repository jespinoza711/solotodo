from django.db import models
from solonotebooks.cotizador.models import StorageDriveType, StorageDriveRpm
from solonotebooks.cotizador.models import StorageDriveCapacity

class StorageDrive(models.Model):
    read_speed = models.IntegerField()
    write_speed = models.IntegerField()
    drive_type = models.ForeignKey(StorageDriveType)
    rpm = models.ForeignKey(StorageDriveRpm)
    capacity = models.ForeignKey(StorageDriveCapacity)
    
    def __unicode__(self):
        result = unicode(self.drive_type) + ' ' + unicode(self.capacity)
        if (self.drive_type.name == 'HDD'):
            result += ' (' + unicode(self.rpm) + ')'
        return result
        
    def rawText(self):
        result = unicode(self.drive_type) + ' ' + unicode(self.capacity)
        if (self.drive_type.name == 'HDD'):
            result += ' ' + unicode(self.rpm)
        return result        
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Storage drive'
        ordering = ['drive_type', 'capacity', 'rpm']
