import utils
from django.db import models
from solonotebooks.cotizador.models import Notebook, Store

class StoreHasNotebook(models.Model):
    url = models.URLField()
    custom_name = models.CharField(max_length = 255)
    is_available = models.BooleanField()
    is_hidden = models.BooleanField()
    visitorCount = models.IntegerField()
    latest_price = models.IntegerField()
    
    notebook = models.ForeignKey(Notebook, null = True, blank = True)
    store = models.ForeignKey(Store)
    
    def __unicode__(self):
        return unicode(self.store) + ' - ' + self.custom_name
        
    def prettyPrice(self):
        return utils.prettyPrice(self.latest_price)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store has notebook'
