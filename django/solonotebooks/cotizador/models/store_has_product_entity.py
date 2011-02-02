from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from solonotebooks.cotizador.models import Notebook, Store, StoreHasProduct
from utils import prettyPrice

class StoreHasProductEntity(models.Model):
    url = models.TextField()
    custom_name = models.CharField(max_length = 255)
    is_available = models.BooleanField()
    is_hidden = models.BooleanField()
    latest_price = models.IntegerField()
    comparison_field = models.TextField()    

    shn = models.ForeignKey(StoreHasProduct, null = True, blank = True)
    
    # uncomment before script
    # prevent_availability_change = models.BooleanField()
    # store = models.ForeignKey(Store)
    # notebook = models.ForeignKey(Notebook, null = True, blank = True)
    
    def __unicode__(self):
        try:
            return unicode(self.shn.store) + ' - ' + self.custom_name
        except:
            return self.custom_name
        
    def pretty_price(self):
        return prettyPrice(self.latest_price)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store has product entity' 
