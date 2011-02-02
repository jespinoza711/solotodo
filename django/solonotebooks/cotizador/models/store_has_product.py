from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from solonotebooks.cotizador.models import Notebook, Store
from utils import prettyPrice

class StoreHasProduct(models.Model):
    # comment next line before script    
    prevent_availability_change = models.BooleanField()
    notebook = models.ForeignKey(Notebook, null = True, blank = True)
    shne = models.ForeignKey('StoreHasProductEntity', null = True, blank = True)
    store = models.ForeignKey(Store)
    
    def __unicode__(self):
        return unicode(self.store) + ' - ' + unicode(self.notebook)
        
    def pretty_price(self):
        return prettyPrice(self.latest_price)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store has product' 
