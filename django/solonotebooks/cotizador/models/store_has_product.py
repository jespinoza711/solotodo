from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from . import Product, Store
from utils import prettyPrice

class StoreHasProduct(models.Model):
    prevent_availability_change = models.BooleanField()
    product = models.ForeignKey(Product, null = True, blank = True)
    shpe = models.ForeignKey('StoreHasProductEntity', null = True, blank = True)
    
    def get_store(self):
        return self.shpe.store
    
    store = property(get_store)
    
    def update(self, recursive = False):
        print self
        shpes = self.storehasproductentity_set.filter(is_available = True).filter(is_hidden = False).order_by('latest_price')
        if shpes:
            self.shpe = shpes[0]
        else:
            self.shpe = None
            
        self.save()
        
        if self.product and recursive:
            self.product.update()
    
    def __unicode__(self):
        return unicode(self.store) + ' - ' + unicode(self.product)
        
    def pretty_price(self):
        return prettyPrice(self.latest_price)
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store has product' 
