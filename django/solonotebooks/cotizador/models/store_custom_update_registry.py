from django.db import models
from . import Store

class StoreCustomUpdateRegistry(models.Model):
    store = models.ForeignKey(Store)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(default='', max_length=255)
    
    def __unicode__(self):
        return unicode(self.store) + ' - ' + str(self.start_datetime)
        
    class Meta:
        app_label = 'cotizador'
