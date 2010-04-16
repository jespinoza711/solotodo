from django.db import models

class StorageDriveCapacity(models.Model):
    value = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.value) + ' GB'
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Storage drive capacity'
        verbose_name_plural = 'Storage drive capacities'
        ordering = ['value']
