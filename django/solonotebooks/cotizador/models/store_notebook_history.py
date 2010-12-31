import utils
from django.db import models
from store_has_notebook_entity import StoreHasNotebookEntity

class StoreNotebookHistory(models.Model):
    price = models.IntegerField()
    date = models.DateField()
    
    registry = models.ForeignKey(StoreHasNotebookEntity)
    
    def __unicode__(self):
        return unicode(self.registry) + ' - ' + unicode(self.date)
        
    def prettyPrice(self):
        utils.prettyPrice(self.price)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store notebook history'
        verbose_name_plural = 'Store notebook histories'
