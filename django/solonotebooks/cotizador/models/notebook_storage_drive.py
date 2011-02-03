from django.db import models
from . import NotebookStorageDriveType, NotebookStorageDriveRpm
from . import NotebookStorageDriveCapacity

class NotebookStorageDrive(models.Model):
    read_speed = models.IntegerField()
    write_speed = models.IntegerField()
    drive_type = models.ForeignKey(NotebookStorageDriveType)
    rpm = models.ForeignKey(NotebookStorageDriveRpm)
    capacity = models.ForeignKey(NotebookStorageDriveCapacity)
    
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
        verbose_name = 'Notebook storage drive'
        ordering = ['drive_type', 'capacity', 'rpm']
