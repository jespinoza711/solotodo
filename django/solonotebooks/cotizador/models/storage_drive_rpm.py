from django.db import models

class StorageDriveRpm(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' rpm'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Storage drive RPM'
        verbose_name_plural = 'Storage drive RPM'
        ordering = ['value']
