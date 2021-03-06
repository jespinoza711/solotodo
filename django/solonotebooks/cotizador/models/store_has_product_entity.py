from django.db import models
from django.db.models import Min, Max, Q
from sorl.thumbnail.fields import ImageWithThumbnailsField
from . import Product, Store, StoreHasProduct, ProductType
from utils import prettyPrice
from datetime import date
from django.contrib.auth.models import User

class StoreHasProductEntity(models.Model):
    url = models.TextField()
    custom_name = models.CharField(max_length = 255)
    part_number = models.CharField(blank=True, null=True, max_length=20)
    is_available = models.BooleanField()
    is_hidden = models.BooleanField()
    latest_price = models.IntegerField()
    comparison_field = models.TextField()
    store = models.ForeignKey(Store)
    prevent_availability_change = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add = True)
    date_resolved = models.DateTimeField(blank = True, null = True)

    shp = models.ForeignKey(StoreHasProduct, null = True, blank = True)
    ptype = models.ForeignKey(ProductType, null = True, blank = True)
    
    resolved_by = models.ForeignKey(User, blank=True, null=True)
    
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
            
    def dprint(self):
        message = str(self.id) + ' ' + unicode(self) + '\n' + self.url + '\n'
        if self.is_available:
            message += 'Disponible'
        else:
            message += 'No disponible'
        return message + '\n'
        
    def pretty_price(self):
        return prettyPrice(self.latest_price)
        
    def delete(self):
        shp = None
        if self.shp:
            shp = self.shp
            if shp.shpe == self:
                shp.shpe = None
                shp.save()
        super(StoreHasProductEntity, self).delete()
        if shp:
            shp.update(recursive = True)
        
    def update(self, recursive = False, product_visits=None):
        from . import LogLostEntity, LogChangeEntityPrice
        print ''
        print str(self)
        print 'Buscando logs de registro'
        last_logs = self.storeproducthistory_set.order_by('-date')
        if last_logs:    
            last_log = last_logs[0]
            if last_log.date != date.today():
                print 'Ultimo registro no es de hoy'
                if self.prevent_availability_change:
                    print 'Registro esta protegido por error de fetching'
                else:
                    print 'Revisando disponibilidad anterior'
                    if self.is_available:
                        print 'Antes estaba disponible, registrando en log'
                        self.is_available = False
                        LogLostEntity.new(self).save()
                        self.save()
                    else:
                        print 'Antes no estaba disponible, no haciendo nada'
            else:
                print 'Ultimo registro es de hoy, viendo si hay cambios de precio entre ayer y hoy'
                try:
                    yesterday_log = last_logs[1]
                    
                    # The second condition helps when executing the "manual_update" script many times
                    # in a single day, preventing repeated log messages
                    if yesterday_log.price != last_log.price and last_log.price != self.latest_price:
                        print 'Hubieron cambios de precio, registrando'
                        LogChangeEntityPrice.new(self, yesterday_log.price, last_log.price).save()
                    else:
                        print 'No hubieron cambios'
                except IndexError:
                    pass
            self.latest_price = last_log.price
            self.save()
        else:
            if self.is_available:
                self.is_available = False
        self.save()
        
        if self.shp and recursive:
            self.shp.update(recursive=True, product_visits=product_visits)
            
    def delete_today_history(self):
        from . import StoreProductHistory
        try:
            sph = StoreProductHistory.objects.get(date = date.today(), registry = self)
            sph.delete()
        except StoreProductHistory.DoesNotExist:
            pass
            
    def retrieve_product(self):
        from solonotebooks.fetch_scripts import *
        fetch_store = eval(self.store.classname + '()')
        return fetch_store.retrieve_product_data(self.url)
            
    def update_price(self):
        product = self.retrieve_product()
        if product:
            self.update_with_product(product)
        else:
            self.delete_today_history()
        self.update(recursive = True)
            
    def update_with_product(self, product):
        from . import StoreProductHistory, LogReviveEntity, LogChangeEntityName
    
        if hasattr(product, 'part_number'):
            self.part_number = product.part_number
        
        if self.custom_name != product.custom_name:
            LogChangeEntityName.new(self, self.custom_name, product.custom_name)
            self.custom_name = product.custom_name
        
        print 'Viendo si esta registrado como desaparecido'
        if not self.is_available:
            print 'Estaba desaparecido, registrando resucitacion'
            LogReviveEntity.new(self).save()
            self.is_available = True
            
        print 'Guardando estado del producto en tienda'
        self.save()

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
