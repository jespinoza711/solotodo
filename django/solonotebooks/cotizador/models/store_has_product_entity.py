from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from . import Product, Store, StoreHasProduct
from utils import prettyPrice
from datetime import date

class StoreHasProductEntity(models.Model):
    url = models.TextField()
    custom_name = models.CharField(max_length = 255)
    is_available = models.BooleanField()
    is_hidden = models.BooleanField()
    latest_price = models.IntegerField()
    comparison_field = models.TextField()
    store = models.ForeignKey(Store)

    shp = models.ForeignKey(StoreHasProduct, null = True, blank = True)
    
    def infer_store(self):
        for store in Store.objects.all():
            if store.url in self.url:
                return store
        return None
    
    def __unicode__(self):
        try:
            return unicode(self.shp.store) + ' - ' + self.custom_name
        except:
            return self.custom_name
        
    def pretty_price(self):
        return prettyPrice(self.latest_price)
        
    def update(self, recursive = False):
        from . import LogLostEntity, LogChangeEntityPrice
        print ''
        print str(self)
        if self.is_available and self.shp and not self.shp.prevent_availability_change:
            print 'Buscando logs de registro'
            last_logs = self.storeproducthistory_set.order_by('-date')
            try:    
                last_log = last_logs[0]
                if not last_log.date == (date.today()):
                    print 'Ultimo registro no es de hoy, dejando entrada no disponible'
                    self.is_available = False
                    LogLostEntity.new(self).save()
                    self.save()
                else:
                    print 'Ultimo registro es de hoy, viendo si hay cambios'
                    try:
                        yesterday_log = last_logs[1]
                        
                        # The second condition helps when executing the "manual_update" script many times
                        # in a single day, preventing repeated log messages
                        if yesterday_log.price != last_log.price and last_log.price != self.latest_price:
                            print 'Hubieron cambios de precio, registrando'
                            self.latest_price = last_log.price
                            self.save()
                            LogChangeEntityPrice.new(self, yesterday_log.price, last_log.price).save()
                        else:
                            print 'No hay cambios'
                    except IndexError:
                        pass
            except IndexError:
                pass
        self.save()
        
        if self.shp and recursive:
            self.shp.update(recursive = True)
            
    def update_price(self):
        pass
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store has product entity' 
