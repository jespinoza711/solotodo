import os, sys, traceback
from solonotebooks.logger import Logger
from datetime import date
from django.db.models import Q
from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
from solonotebooks import settings

class Store(models.Model):
    name = models.CharField(max_length = 255)
    classname = models.CharField(max_length = 255)
    url = models.URLField()
    sponsor_cap = models.IntegerField(default = 0)
    picture = ImageWithThumbnailsField(
        thumbnail = { 'size': (140, 90), },                                          
        upload_to = 'store_logos',
        generate_on_save = True,)
    
    def fetch_store(self):
        from solonotebooks.fetch_scripts import *
        return eval(self.classname + '()')
    
    def __unicode__(self):
        return unicode(self.name)
        
    def fetch_product_data(self, url):
        from . import StoreHasProductEntity
        from solonotebooks.fetch_scripts import *
        fetch_store = self.fetch_store()
        product = fetch_store.retrieve_product_data(url)
        if not product:
            return None
        else:
            shpes = StoreHasProductEntity.objects.filter(custom_name = product.custom_name, store = self)
            if shpes:
                return shpes[0]
            else:
                return None
        
    def save_product(self, product):
        from . import StoreHasProductEntity, LogNewEntity, ProductType
        print 'Guardando ' + str(product)
        print 'Buscando si tiene un registro existente'
        try:
            shpe = StoreHasProductEntity.objects.get(comparison_field = product.comparison_field)
            print 'Si tiene registro existente, usandolo'
        except StoreHasProductEntity.DoesNotExist:
            print 'No tiene registro existente, creandolo'
            shpe = StoreHasProductEntity()
            shpe.url = product.url
            shpe.custom_name = product.custom_name
            shpe.comparison_field = product.comparison_field
            shpe.shp = None
            shpe.is_available = True
            shpe.is_hidden = False
            shpe.latest_price = product.price
            shpe.store = self
            try:
                ptype = ProductType.objects.get(classname = product.ptype)
                shpe.ptype = ptype
            except:
                pass
            shpe.save()
            LogNewEntity.new(shpe).save()
            
        shpe.update_with_product(product)
        
    def update_products_from_webpage(self, update_shpes_on_finish = False):
        from . import LogFetchStoreError
        fetch_store = self.fetch_store()
        fetch_log_file_location = os.path.join(settings.LOG_DIRECTORY, fetch_store.__class__.__name__ + '_fetch.txt')
        logger = Logger(sys.stdout, fetch_log_file_location)
        sys.stdout = logger
        
        try:
            store = Store.objects.get(name = fetch_store.name)
        except Store.DoesNotExist:
            store = Store()
            store.name = fetch_store.name
            store.save()
            
        store.set_shpe_prevent_availability_change_flag(False)
            
        try:
            if update_shpes_on_finish:
                for shpe in store.storehasproductentity_set.all():
                    shpe.delete_today_history()
            
            products = fetch_store.get_products()        
            
            update_log_file_location = os.path.join(settings.LOG_DIRECTORY, fetch_store.__class__.__name__ + '_update.txt')
            print update_log_file_location
            logger.change_log_file(update_log_file_location)
            for product in products:
                self.save_product(product)
            
            if update_shpes_on_finish:
                for shpe in store.storehasproductentity_set.all():
                    shpe.update(recursive = True)

            try:                
                log_error = LogFetchStoreError.objects.get(log_entry__date = date.today(), store = store)
                log_error.delete()
            except LogFetchStoreError.DoesNotExist, e:
                pass
                
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            print e
            print('Error al obtener los productos de ' + store.name)
            
            try:                
                log_error = LogFetchStoreError.objects.get(log_entry__date = date.today(), store = store)
            except LogFetchStoreError.DoesNotExist, ex:
                LogFetchStoreError.new(store, str(e))
            
            store.set_shpe_prevent_availability_change_flag(True)
            
        sys.stdout = logger.default_stdout()
        
    def set_shpe_prevent_availability_change_flag(self, flag):
        from . import StoreHasProductEntity
        shpes = StoreHasProductEntity.objects.filter(store = self)
        for shpe in shpes:
            shpe.prevent_availability_change = flag
            shpe.save()
            
    def get_products_in_category(self, ptype, ordering):
        from . import StoreHasProductEntity, StoreHasProduct
        classname = ptype.get_class()
        products = classname.get_available()
        
        shps = StoreHasProduct.objects.filter(shpe__store = self, product__in = products)
        
        if ordering == '1':
            shps = shps.order_by('product__display_name')
        elif ordering == '2':
            shps = shps.order_by('-product__week_visitor_count')
        elif ordering == '3':
            shps = shps.order_by('-product__week_external_visits')
        
        final_products = []    
        for shp in shps:
            shp.product.store_shpe = shp.shpe
            
            other_shps = StoreHasProduct.objects.filter(product = shp.product, shpe__isnull=False).filter(~Q(shpe__store = self)).order_by('shpe__latest_price')
            if other_shps:
                shp.product.competitor_shps = other_shps[:3]
            else:
                shp.product.competitor_shps = []
                
            final_products.append(shp.product)
            
        return final_products
    
    class Meta:
        ordering = ['name']
        app_label = 'cotizador'
        verbose_name = 'Store'
