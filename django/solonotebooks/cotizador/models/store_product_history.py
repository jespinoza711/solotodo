import utils
from django.db import models
from . import StoreHasProductEntity

class StoreProductHistory(models.Model):
    price = models.IntegerField()
    date = models.DateField(db_index=True)
    
    registry = models.ForeignKey(StoreHasProductEntity)
    
    def __unicode__(self):
        return unicode(self.registry) + ' - ' + unicode(self.date)
        
    def prettyPrice(self):
        utils.prettyPrice(self.price)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store product history'
        verbose_name_plural = 'Store product histories'
