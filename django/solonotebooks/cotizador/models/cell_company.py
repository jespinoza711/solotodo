from django.db import models
from . import Store

class CellCompany(models.Model):
    store = models.ForeignKey(Store)
    fetch_store = property(lambda self: self.store.fetch_store())
    
    def __unicode__(self):
        return unicode(self.store)
        
    def raw_text(self):
        return unicode(self)      
    
    class Meta:
        app_label = 'cotizador'
        ordering = ['store']
