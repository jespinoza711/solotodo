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
        from solonotebooks.fetch_scripts import *
        fetch_store = eval(self.store.classname + '()')
        product = fetch_store.retrieve_product_data(self.url)
        if product:
            self.update_with_product(product)
        else:
            self.is_available = False
        self.update(recursive = True)
            
    def update_with_product(self, product):
        from . import StoreProductHistory
        print 'Viendo si esta registrado como desaparecido'
        if not self.is_available:
            print 'Estaba desaparecido, registrando resucitacion'
            LogReviveEntity.new(self).save()
            self.is_available = True
            
        print 'Guardando estado del producto en tienda'
        self.save()

        # We keep track of prices for every day, and we need to avoid clashes
        print 'Viendo si ya se solicito un catastro para hoy'
        today_history = StoreProductHistory.objects.filter(date = date.today()).filter(registry = self)
        if len(today_history) == 0:
            print 'No hay registro de hoy, creandolo'
            snh = StoreProductHistory()
            snh.price = product.price
            snh.date = date.today()
            snh.registry = self
            snh.save()    
        else:
            print 'Hay un registro existente, viendo si hay cambios de precio'
            today_history = today_history[0]
            if today_history.price != product.price:
                print 'Hubo un cambio de precio'
                today_history.price = product.price
                today_history.save()
                self.latest_price = product.price
                self.save()
    
    class Meta:
        app_label = 'cotizador'
        verbose_name = 'Store has product entity' 
